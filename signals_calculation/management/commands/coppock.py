import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import CoppockModel  # Assuming CoppockModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Coppock Curve, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol', 'ltp', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_coppock(self, close_prices, short_roc_period=14, long_roc_period=11, wma_period=10):
        """
        Calculate the Coppock Curve based on close prices.
        """
        # Create a pandas series for close prices
        close_prices_series = pd.Series(close_prices)

        # Calculate the Rate of Change (ROC) for both periods
        short_roc = close_prices_series.diff(short_roc_period) / close_prices_series.shift(short_roc_period) * 100
        long_roc = close_prices_series.diff(long_roc_period) / close_prices_series.shift(long_roc_period) * 100

        # Add the two ROC values
        roc_sum = short_roc + long_roc

        # Calculate the Weighted Moving Average (WMA) of the ROC sum
        coppock_curve = roc_sum.rolling(window=wma_period).mean()

        return coppock_curve

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate Coppock Curve values
            coppock_values = self.calculate_coppock(closes)

            # Skip the initial values due to NaN
            for i in range(max(14, 11), len(coppock_values)):
                coppock_value = coppock_values.iloc[i]
                if pd.isna(coppock_value):  # Skip if Coppock is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - Coppock Curve is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Bullish" if coppock_value > 0 else "Bearish"

                # Save to database
                CoppockModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "coppock_value": coppock_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - Coppock: {coppock_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Coppock Curve.")
