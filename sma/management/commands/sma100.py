import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from sma.models import Sma100Model  # Assuming Sma100Model exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate SMA100, and store it in the database'

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

    def calculate_sma(self, close_prices, period=100):
        """
        Calculate the SMA for the given close prices and period.
        """
        # Convert to pandas Series
        close_series = pd.Series(close_prices)

        # Calculate SMA
        sma = close_series.rolling(window=period).mean()

        return sma

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate SMA100 values
            sma_values = self.calculate_sma(closes, period=100)

            # Iterate through the SMA values
            for i in range(len(sma_values)):
                sma_value = sma_values.iloc[i]
                if pd.isna(sma_value):  # Skip if SMA is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - SMA100 is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal (e.g., above SMA for "Buy" or below for "Sell")
                signal = "Buy" if closes[i] > sma_value else "Sell"

                # Save to database
                Sma100Model.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "sma_100_value": sma_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - SMA100: {sma_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate SMA100.")
