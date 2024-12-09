import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import EriModel  # Assuming EriModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Elder Ray Index (ERI), and store it in the database'

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

    def calculate_eri(self, high_prices, low_prices, close_prices, period=13):
        """
        Calculate the Elder Ray Index (ERI) values based on the high, low, and close prices.
        """
        # Calculate the 13-period EMA of the close prices
        ema_close = pd.Series(close_prices).ewm(span=period, adjust=False).mean()

        # Calculate Bull Power and Bear Power
        bull_power = pd.Series(high_prices) - ema_close
        bear_power = pd.Series(low_prices) - ema_close

        # Return the Bull Power and Bear Power
        return bull_power, bear_power

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            highs = [float(item["high"]) for item in data]
            lows = [float(item["low"]) for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate Bull Power and Bear Power (ERI components)
            bull_power, bear_power = self.calculate_eri(highs, lows, closes)

            # Iterate through the data to determine signals and save them
            for i in range(len(bull_power)):
                bull_value = bull_power.iloc[i]
                bear_value = bear_power.iloc[i]

                # Determine the signal based on the Bull Power and Bear Power
                if bull_value > 0 and bear_value < 0:
                    signal = "Bullish"
                elif bull_value < 0 and bear_value > 0:
                    signal = "Bearish"
                else:
                    signal = "Neutral"

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Save to the database
                EriModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "bull_power": bull_value,
                        "bear_power": bear_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - Bull Power: {bull_value:.4f}, Bear Power: {bear_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Elder Ray Index.")
