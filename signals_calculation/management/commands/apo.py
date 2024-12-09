import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import ApoModel  # Assuming ApoModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate APO, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values('symbol', 'ltp', 'datetime')
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_apo(self, prices, short_period=12, long_period=26):
        """
        Calculate the Absolute Price Oscillator (APO) based on close prices.
        """
        short_ema = pd.Series(prices).ewm(span=short_period, adjust=False).mean()
        long_ema = pd.Series(prices).ewm(span=long_period, adjust=False).mean()

        # APO is the difference between the short EMA and the long EMA
        apo = short_ema - long_ema
        return apo

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate APO values
            apo_values = self.calculate_apo(closes)

            # Skip the first few values (due to NaN from EMA calculation)
            for i in range(max(12, 26), len(apo_values)):
                apo_value = apo_values.iloc[i]
                if pd.isna(apo_value):  # Skip if APO is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - APO is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Bullish" if apo_value > 0 else "Bearish" if apo_value < 0 else "Neutral"

                # Save to database
                ApoModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "apo_value": apo_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - APO: {apo_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate APO.")
