import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import ROCModel  # Assuming ROCModel exists for storing ROC data
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from django.db.models import Max


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate ROC, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch data from the database ordered by datetime.
        """
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol', 'high', 'low','ltp', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []
        

    def calculate_roc(self, closes, period=14):
        """
        Calculate the Rate of Change (ROC) for the given closing prices.
        """
        # Ensure the closing prices are in a pandas Series
        closes_series = pd.Series(closes)

        # Calculate the ROC
        roc = ((closes_series - closes_series.shift(period)) / closes_series.shift(period)) * 100

        return roc

    def calculate_signal(self, roc_value):
        """
        Generate a signal based on the ROC value.
        """
        if roc_value > 0:
            return "Positive"
        elif roc_value < 0:
            return "Negative"
        else:
            return "Neutral"

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if not data:
            self.stdout.write("No data fetched from the database.")
            return

        self.stdout.write(f"Fetched {len(data)} data points.")

        # Extract fields
        symbols = [item["symbol"] for item in data]
        closes = [float(item["ltp"]) for item in data]
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if not (len(symbols) == len(closes) == len(timestamps)):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Calculate ROC values
            roc_values = self.calculate_roc(closes)

            # Skip NaN values (initial values for ROC calculation)
            for i in range(14, len(roc_values)):
                roc_value = roc_values.iloc[i]

                if pd.isna(roc_value):  # Skip if ROC is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - ROC is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal based on ROC value
                signal = self.calculate_signal(roc_value)

                # Save to database
                ROCModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "roc": roc_value,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - ROC: {roc_value:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating ROC: {str(e)}")
