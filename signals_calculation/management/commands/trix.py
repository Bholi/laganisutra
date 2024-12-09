import pandas as pd
from django.core.management.base import BaseCommand
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from momentum.models import TrixModel  # Assuming TrixModel exists to store the TRIX results
from django.db.models import Max
class Command(BaseCommand):
    help = 'Fetch data from DB, calculate TRIX, and store it in the database'

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

    def calculate_trix(self, close_prices, period=14):
        """
        Calculate the TRIX (Triple Exponential Moving Average) value based on closing prices.
        """
        # Calculate the first EMA (single EMA)
        ema1 = pd.Series(close_prices).ewm(span=period).mean()

        # Calculate the second EMA (double EMA)
        ema2 = ema1.ewm(span=period).mean()

        # Calculate the third EMA (triple EMA)
        ema3 = ema2.ewm(span=period).mean()

        # Calculate TRIX as the percentage change in triple EMA
        trix = ema3.pct_change() * 100  # The result is a percentage change

        return trix

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate TRIX values
            trix_values = self.calculate_trix(closes)

            # Skip the first value (due to NaN from pct_change)
            for i in range(1, len(trix_values)):
                trix_value = trix_values.iloc[i]
                if pd.isna(trix_value):  # Skip if TRIX is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - TRIX is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Bullish" if trix_value > 0 else "Bearish"

                # Save to database
                TrixModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "trix_value": trix_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - TRIX: {trix_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate TRIX.")
