import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import CfoModel  # Assuming CfoModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Chande Forecast Oscillator (CFO), and store it in the database'

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

    def calculate_cfo(self, close_prices, period=14):
        """
        Calculate Chande Forecast Oscillator (CFO) over a given period.
        """
        # Create a pandas series for close prices
        close_prices_series = pd.Series(close_prices)

        # Calculate linear regression forecast using rolling window
        forecast = close_prices_series.rolling(window=period).apply(
            lambda x: pd.Series(x).reset_index(drop=True).cov(pd.Series(range(len(x)))) /
                      pd.Series(range(len(x))).var() * (len(x) - 1) +
                      x.mean(),
            raw=False
        )

        # Calculate CFO
        cfo = ((close_prices_series - forecast) / close_prices_series) * 100

        return cfo

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate CFO values
            cfo_values = self.calculate_cfo(closes) 

            # Skip the first 14 values (due to NaN from rolling window)
            for i in range(14, len(cfo_values)):
                cfo_value = cfo_values.iloc[i]
                if pd.isna(cfo_value):  # Skip if CFO is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - CFO is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                if cfo_value > 0:
                    signal = "Bullish"
                elif cfo_value < 0:
                    signal = "Bearish"
                else:
                    signal = "Neutral"

                # Save to database
                CfoModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "cfo_value": cfo_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - CFO: {cfo_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate CFO.")
