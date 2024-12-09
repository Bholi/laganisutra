import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import CgModel  # Assuming CgModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate CG, and store it in the database'

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

    def calculate_cog(self, prices, period=10):
        """
        Calculate the Center of Gravity (CG) value based on the closing prices.
        """
        prices = pd.Series(prices)
        weights = range(1, period + 1)

        # Calculate the weighted moving average (Center of Gravity)
        cog = prices.rolling(window=period).apply(
            lambda x: -sum(weights[i] * x[i] for i in range(len(weights))) / sum(weights),
            raw=True
        )

        return cog

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate CoG values
            cog_values = self.calculate_cog(closes)

            # Skip the first period values (due to NaN from rolling window)
            period = 10
            for i in range(period, len(cog_values)):
                cog_value = cog_values.iloc[i]
                if pd.isna(cog_value):  # Skip if CoG is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - CG is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Buy" if cog_value > 0 else "Sell"

                # Save to database
                CgModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "cg_value": cog_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - CG: {cog_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate CG.")
