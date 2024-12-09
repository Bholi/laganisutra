import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import InertiaModel  # Assuming InertiaModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Inertia, and store it in the database'

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

    def calculate_inertia(self, prices, period=14):
        """
        Calculate the Inertia indicator based on the closing prices.
        """
        prices = pd.Series(prices)

        # Calculate the Linear Regression Slope (LRS)
        slopes = prices.rolling(window=period).apply(
            lambda x: pd.Series(x).reset_index(drop=True).corr(pd.Series(range(len(x)))),
            raw=True
        )

        # Smooth the LRS to calculate Inertia
        inertia = slopes.rolling(window=period).mean()
        return inertia

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate Inertia values
            inertia_values = self.calculate_inertia(closes)

            # Skip the first period values (due to NaN from rolling window)
            period = 14
            for i in range(period, len(inertia_values)):
                inertia_value = inertia_values.iloc[i]
                if pd.isna(inertia_value):  # Skip if Inertia is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - Inertia is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Trend" if abs(inertia_value) > 0.5 else "No Trend"

                # Save to database
                InertiaModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "inertia": inertia_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - Inertia: {inertia_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Inertia.")
