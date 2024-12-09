import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import BiasModel  # Assuming BiasModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Bias, and store it in the database'

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

    def calculate_bias(self, prices, moving_avg_period=14):
        """
        Calculate the Bias based on the current prices and a moving average.
        """
        # Calculate the moving average
        moving_avg = pd.Series(prices).rolling(window=moving_avg_period).mean()

        # Calculate Bias = ((Price - Moving Average) / Moving Average) * 100
        bias = ((pd.Series(prices) - moving_avg) / moving_avg) * 100
        return bias

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate Bias values
            bias_values = self.calculate_bias(closes)

            # Skip the first few values (due to NaN from moving average calculation)
            for i in range(14, len(bias_values)):
                bias_value = bias_values.iloc[i]
                if pd.isna(bias_value):  # Skip if Bias is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - Bias is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = (
                    "Overbought" if bias_value > 5 else
                    "Oversold" if bias_value < -5 else
                    "Neutral"
                )

                # Save to database
                BiasModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "bias_value": bias_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - Bias: {bias_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Bias.")
