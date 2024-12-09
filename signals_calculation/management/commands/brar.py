import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import BrarModel  # Assuming BrarModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate BRAR, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol', 'high', 'low', 'open', 'ltp', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_brar(self, highs, lows, opens, closes, period=14):
        """
        Calculate BR and AR over a given period.
        """
        # Initialize BR and AR lists
        br_values = []
        ar_values = []

        for i in range(1, len(highs)):
            high = highs[i]
            low = lows[i]
            prev_close = closes[i - 1]
            open_price = opens[i]

            # Calculate BR numerator and denominator
            br_numerator = max(0, high - prev_close)
            br_denominator = max(0, prev_close - low)

            # Calculate AR numerator and denominator
            ar_numerator = max(0, high - open_price)
            ar_denominator = max(0, open_price - low)

            # Avoid division by zero
            br = br_numerator / br_denominator if br_denominator != 0 else 0
            ar = ar_numerator / ar_denominator if ar_denominator != 0 else 0

            br_values.append(br)
            ar_values.append(ar)

        # Smooth BR and AR over the given period
        br_series = pd.Series(br_values).rolling(window=period).mean()
        ar_series = pd.Series(ar_values).rolling(window=period).mean()

        return br_series, ar_series

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            highs = [float(item["high"]) for item in data]
            lows = [float(item["low"]) for item in data]
            opens = [float(item["open"].replace(',', '')) for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate BRAR values
            br_values, ar_values = self.calculate_brar(highs, lows, opens, closes)

            # Skip the first 14 values (due to NaN from rolling window)
            for i in range(14, len(br_values)):
                br_value = br_values.iloc[i]
                ar_value = ar_values.iloc[i]
                if pd.isna(br_value) or pd.isna(ar_value):  # Skip if BR or AR is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - BRAR is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine sentiment signal
                if br_value > ar_value:
                    signal = "Bullish"
                elif br_value < ar_value:
                    signal = "Bearish"
                else:
                    signal = "Neutral"

                # Save to database
                BrarModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "br_value": br_value,
                        "ar_value": ar_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - BR: {br_value:.4f}, AR: {ar_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate BRAR.")
