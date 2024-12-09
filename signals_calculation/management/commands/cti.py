import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import CtiModel  # Assuming CtiModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate CTI, and store it in the database'

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

    def calculate_cti(self, close_prices, period=20):
        """
        Calculate the Correlation Trend Indicator (CTI).
        """
        # Create a pandas series for close prices
        close_prices_series = pd.Series(close_prices)

        # Calculate the mean of the close prices over the period
        rolling_mean = close_prices_series.rolling(window=period).mean()

        # Calculate the standard deviation of the close prices over the period
        rolling_std = close_prices_series.rolling(window=period).std()

        # Calculate z-scores
        z_scores = (close_prices_series - rolling_mean) / rolling_std

        # Normalize CTI to range [-1, 1]
        cti = z_scores.clip(-2, 2) / 2  # Divide by 2 to scale z-scores to [-1, 1]

        return cti

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate CTI values
            cti_values = self.calculate_cti(closes)

            # Skip the initial values due to NaN
            for i in range(20, len(cti_values)):
                cti_value = cti_values.iloc[i]
                if pd.isna(cti_value):  # Skip if CTI is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - CTI is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                if cti_value > 0.5:
                    signal = "Bullish"
                elif cti_value < -0.5:
                    signal = "Bearish"
                else:
                    signal = "Neutral"

                # Save to database
                CtiModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "cti_value": cti_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - CTI: {cti_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate CTI.")
