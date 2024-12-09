import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from ema.models import Ema20Model  # Assuming Ema20Model exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate EMA20, and store it in the database'

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

    def calculate_ema(self, close_prices, period=20):
        """
        Calculate the EMA for the given close prices and period.
        """
        # Convert to pandas Series
        close_series = pd.Series(close_prices)

        # Calculate EMA
        ema = close_series.ewm(span=period, adjust=False).mean()

        return ema

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate EMA20 values
            ema_values = self.calculate_ema(closes, period=20)

            # Iterate through the EMA values
            for i in range(len(ema_values)):
                ema_value = ema_values.iloc[i]
                if pd.isna(ema_value):  # Skip if EMA is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - EMA20 is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal (e.g., above a threshold for "Buy" or below for "Sell")
                signal = "Buy" if closes[i] > ema_value else "Sell"

                # Save to database
                Ema20Model.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "ema_20_value": ema_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - EMA20: {ema_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate EMA20.")
