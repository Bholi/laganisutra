import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import RSXModel  # Assuming RSXModel exists for storing RSX data
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from django.db.models import Max


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate RSX, and store it in the database'

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
        Calculate the Relative Strength Index (RSI).
        """
        delta = pd.Series(closes).diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period, min_periods=1).mean()
        avg_loss = loss.rolling(window=period, min_periods=1).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate_rsx(self, closes, period=14, smoothing_period=3):
        """
        Calculate the RSX (Relative Strength Xtra).
        """
        # Calculate the RSI
        rsi = self.calculate_rsi(closes, period)
        
        # Apply an EMA to smooth the RSI values
        rsx = rsi.ewm(span=smoothing_period, adjust=False).mean()

        return rsx

    def calculate_signal(self, rsx_value):
        """
        Generate a signal based on the RSX value.
        """
        if rsx_value > 70:
            return "Overbought"
        elif rsx_value < 30:
            return "Oversold"
        else:
            return "Neutral"

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
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if not (len(symbols) == len(closes) == len(timestamps)):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Calculate RSX values
            rsx_values = self.calculate_rsx(closes)

            # Skip NaN values (initial values for RSX calculation)
            for i in range(14, len(rsx_values)):
                rsx_value = rsx_values.iloc[i]

                if pd.isna(rsx_value):  # Skip if RSX is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - RSX is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal based on RSX value
                signal = self.calculate_signal(rsx_value)

                # Save to database
                RSXModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "rsx": rsx_value,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - RSX: {rsx_value:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating RSX: {str(e)}")
