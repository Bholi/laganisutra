import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import DmModel  # Assuming DmModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Directional Movement (DM), and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol', 'high', 'low', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_dm(self, high_prices, low_prices):
        """
        Calculate Directional Movement (+DM, -DM) and their signals.
        """
        plus_dm = []
        minus_dm = []
        signals = []

        for i in range(1, len(high_prices)):
            high_diff = high_prices[i] - high_prices[i - 1]
            low_diff = low_prices[i - 1] - low_prices[i]

            plus = max(0, high_diff) if high_diff > low_diff else 0
            minus = max(0, low_diff) if low_diff > high_diff else 0

            plus_dm.append(plus)
            minus_dm.append(minus)

            # Determine signal: Bullish if +DM > -DM, Bearish if -DM > +DM
            if plus > minus:
                signals.append("Bullish")
            elif minus > plus:
                signals.append("Bearish")
            else:
                signals.append("Neutral")

        return plus_dm, minus_dm, signals

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            highs = [float(item["high"]) for item in data]
            lows = [float(item["low"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate Directional Movement values and signals
            plus_dm, minus_dm, signals = self.calculate_dm(highs, lows)

            # Skip the first value (no comparison for the first point)
            for i in range(1, len(plus_dm)):
                symbol = symbols[i]
                timestamp = timestamps[i]
                plus_dm_value = plus_dm[i - 1]
                minus_dm_value = minus_dm[i - 1]
                signal = signals[i - 1]

                # Save to database
                DmModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "plus_dm": plus_dm_value,
                        "minus_dm": minus_dm_value,
                        "signal": signal,
                    }
                )

                self.stdout.write(f"Saved {symbol} - +DM: {plus_dm_value:.4f}, -DM: {minus_dm_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Directional Movement.")
