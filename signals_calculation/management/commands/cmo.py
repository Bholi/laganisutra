import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import CmoModel  # Assuming CmoModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Chande Momentum Oscillator (CMO), and store it in the database'

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

    def calculate_cmo(self, close_prices, period=14):
        """
        Calculate the Chande Momentum Oscillator (CMO) over a given period.
        """
        # Create a pandas series for close prices
        close_prices_series = pd.Series(close_prices)

        # Calculate differences between consecutive closing prices
        differences = close_prices_series.diff()

        # Calculate gains and losses
        gains = differences.where(differences > 0, 0)
        losses = -differences.where(differences < 0, 0)

        # Rolling sum of gains and losses over the period
        sum_gains = gains.rolling(window=period).sum()
        sum_losses = losses.rolling(window=period).sum()

        # CMO formula
        cmo = ((sum_gains - sum_losses) / (sum_gains + sum_losses)) * 100

        return cmo

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate CMO values
            cmo_values = self.calculate_cmo(closes)

            # Skip the first `period` values (due to NaN from rolling window)
            for i in range(14, len(cmo_values)):
                cmo_value = cmo_values.iloc[i]
                if pd.isna(cmo_value):  # Skip if CMO is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - CMO is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                if cmo_value > 50:
                    signal = "Overbought"
                elif cmo_value < -50:
                    signal = "Oversold"
                else:
                    signal = "Neutral"

                # Save to database
                CmoModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "cmo_value": cmo_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - CMO: {cmo_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate CMO.")
