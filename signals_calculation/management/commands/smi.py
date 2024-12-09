import pandas as pd
from django.core.management.base import BaseCommand
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from momentum.models import SMIErgodicModel  # Assuming SMIErgodicModel exists for storing SMI data
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate SMI Ergodic, and store it in the database'

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
        

    def calculate_smi(self, high_prices, low_prices, close_prices, period=14, smoothing_period=3):
        """
        Calculate the SMI Ergodic based on high, low, and close prices.
        """
        # Step 1: Calculate Stochastic Oscillator (SO)
        lowest_low = pd.Series(low_prices).rolling(window=period).min()
        highest_high = pd.Series(high_prices).rolling(window=period).max()
        
        # SO calculation
        so = 100 * (pd.Series(close_prices) - lowest_low) / (highest_high - lowest_low)

        # Step 2: Smooth the Stochastic Oscillator using a moving average
        smoothed_so = so.rolling(window=smoothing_period).mean()

        # Step 3: Calculate SMI (difference between smoothed oscillator and midpoint of the price range)
        smi = smoothed_so - (highest_high + lowest_low) / 2

        return smi

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if not data:
            self.stdout.write("No data fetched from the database.")
            return

        self.stdout.write(f"Fetched {len(data)} data points.")

        # Extract fields
        symbols = [item["symbol"] for item in data]
        highs = [float(item["high"]) for item in data]
        lows = [float(item["low"]) for item in data]
        closes = [float(item["ltp"]) for item in data]  # Assuming LTP is used as the close price
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if len(symbols) != len(highs) or len(symbols) != len(lows) or len(symbols) != len(closes) or len(symbols) != len(timestamps):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Calculate SMI Ergodic for each symbol
            for i in range(14, len(closes)):  # Ensure we have enough data for the first period (14)
                symbol = symbols[i]
                timestamp = timestamps[i]
                high_prices_window = highs[i-14:i]  # Last 14 high prices
                low_prices_window = lows[i-14:i]  # Last 14 low prices
                close_prices_window = closes[i-14:i]  # Last 14 closing prices

                # Calculate SMI Ergodic
                smi_value = self.calculate_smi(high_prices_window, low_prices_window, close_prices_window)

                # Determine signal based on SMI
                if smi_value.iloc[-1] > 0:
                    signal = "Buy"
                elif smi_value.iloc[-1] < 0:
                    signal = "Sell"
                else:
                    signal = "Neutral"

                # Save to database
                SMIErgodicModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "smi_ergodic": smi_value.iloc[-1],
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - SMI: {smi_value.iloc[-1]:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating SMI Ergodic: {str(e)}")
