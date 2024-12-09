import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import QqeModel  # Assuming QqeModel exists for storing QQE data
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from django.db.models import Max


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate QQE, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch data from the database ordered by datetime.
        """
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol', 'high', 'low','ltp', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []
       

    def calculate_rsi(self, closes, period=14):
        """
        Calculate RSI (Relative Strength Index) for the given closing prices.
        """
        delta = pd.Series(closes).diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_atr(self, highs, lows, closes, period=14):
        """
        Calculate the Average True Range (ATR) for the given high, low, and close prices.
        """
        tr = pd.concat([highs - lows, abs(highs - closes.shift()), abs(lows - closes.shift())], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr

    def calculate_qqe(self, closes, highs, lows, period=14, atr_period=14, smoothing_factor=5):
        """
        Calculate the QQE (Quantitative Qualitative Estimation) indicator.
        """
        # Step 1: Calculate RSI
        rsi = self.calculate_rsi(closes, period)

        # Step 2: Smooth the RSI with an EMA
        smoothed_rsi = rsi.ewm(span=smoothing_factor, adjust=False).mean()

        # Step 3: Calculate ATR
        atr = self.calculate_atr(highs, lows, closes, atr_period)

        # Step 4: Calculate Fast QQE Line and Slow QQE Line
        fast_qqe = smoothed_rsi + atr
        slow_qqe = smoothed_rsi - atr

        # Step 5: Generate Buy and Sell Signals
        signals = []
        for i in range(1, len(fast_qqe)):
            if fast_qqe.iloc[i] > slow_qqe.iloc[i] and fast_qqe.iloc[i-1] <= slow_qqe.iloc[i-1]:
                signals.append("Buy")
            elif fast_qqe.iloc[i] < slow_qqe.iloc[i] and fast_qqe.iloc[i-1] >= slow_qqe.iloc[i-1]:
                signals.append("Sell")
            else:
                signals.append("Neutral")

        # Fill the signals with "Neutral" for the first few points
        signals = ["Neutral"] * (period - 1) + signals

        return fast_qqe, slow_qqe, signals

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if not data:
            self.stdout.write("No data fetched from the database.")
            return

        self.stdout.write(f"Fetched {len(data)} data points.")

        # Extract fields
        symbols = [item["symbol"] for item in data]
        closes = [float(item["ltp"]) for item in data]
        highs = [float(item["high"]) for item in data]
        lows = [float(item["low"]) for item in data]
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if not (len(symbols) == len(closes) == len(highs) == len(lows) == len(timestamps)):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Convert lists to pandas Series for proper handling
            closes_series = pd.Series(closes)
            highs_series = pd.Series(highs)
            lows_series = pd.Series(lows)

            # Calculate QQE values
            fast_qqe, slow_qqe, signals = self.calculate_qqe(closes_series, highs_series, lows_series)

            # Skip NaN values (initial values for RSI and ATR calculation)
            for i in range(14, len(fast_qqe)):
                fast_qqe_value = fast_qqe.iloc[i]
                slow_qqe_value = slow_qqe.iloc[i]
                signal = signals[i]

                if pd.isna(fast_qqe_value) or pd.isna(slow_qqe_value):
                    self.stdout.write(f"Skipping {symbols[i]} - QQE is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Save to database
                QqeModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "fast_qqe": fast_qqe_value,
                        "slow_qqe": slow_qqe_value,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - Fast QQE: {fast_qqe_value:.4f}, Slow QQE: {slow_qqe_value:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating QQE: {str(e)}")
