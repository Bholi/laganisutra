import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import ErModel  # Assuming ErModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Efficiency Ratio (ER), and store it in the database'

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

    def calculate_er(self, close_prices, period=14):
        """
        Calculate Efficiency Ratio (ER) for a given period.
        """
        if len(close_prices) < period:
            return []

        er_values = []
        for i in range(period, len(close_prices)):
            # Calculate the absolute change (direction) over the period
            direction = abs(close_prices[i] - close_prices[i - period])

            # Calculate the sum of absolute changes (volatility) over the period
            volatility = sum(abs(close_prices[j] - close_prices[j - 1]) for j in range(i - period + 1, i + 1))

            # Calculate ER
            er = direction / volatility if volatility != 0 else 0
            er_values.append(er)

        return [None] * period + er_values  # Add None for initial values

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate Efficiency Ratio values
            er_values = self.calculate_er(closes)

            # Skip None values (initial period without ER values)
            for i in range(len(er_values)):
                er_value = er_values[i]
                if er_value is None:
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal based on ER thresholds
                signal = "Strong Trend" if er_value > 0.5 else "Weak Trend"

                # Save to database
                ErModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "efficiency_ratio": er_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - ER: {er_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Efficiency Ratio.")
