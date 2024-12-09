import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from momentum.models import TsiModel  # Assuming TsiModel exists to store the TSI results

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate TSI (True Strength Index), and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values('symbol', 'high', 'low', 'ltp', 'datetime')
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_tsi(self, close_prices, long_period=25, short_period=13):
        """
        Calculate the True Strength Index (TSI) based on closing prices.
        """
        # Calculate the momentum (difference between current and previous close)
        momentum = pd.Series(close_prices).diff()

        # Calculate the double smoothed momentum
        smoothed_momentum = momentum.ewm(span=short_period).mean().ewm(span=long_period).mean()

        # Calculate the absolute momentum (for price momentum calculation)
        abs_momentum = momentum.abs()

        # Calculate the double smoothed price momentum
        smoothed_abs_momentum = abs_momentum.ewm(span=short_period).mean().ewm(span=long_period).mean()

        # Calculate TSI
        tsi = (smoothed_momentum / smoothed_abs_momentum) * 100

        return tsi

    def handle(self, *args, **kwargs):
        # Define short and long periods for TSI calculation
        short_period = 13  # Short period for smoothing (commonly 13)
        long_period = 25   # Long period for smoothing (commonly 25)

        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate TSI values
            tsi_values = self.calculate_tsi(closes, long_period, short_period)

            # Skip the first two periods (due to NaN from ewm)
            for i in range(max(1, short_period, long_period), len(tsi_values)):
                tsi_value = tsi_values.iloc[i]
                if pd.isna(tsi_value):  # Skip if TSI is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - TSI is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Bullish" if tsi_value > 0 else "Bearish"

                # Save to database
                TsiModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "tsi_value": tsi_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - TSI: {tsi_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate TSI.")
