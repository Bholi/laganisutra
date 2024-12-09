import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import PPOModel  # Assuming PPOModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate PPO, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime__lte=latest_datetime).values(
                'symbol', 'ltp', 'datetime'
            )
            return list(data)
        else:
            return []

    def calculate_ppo(self, close_prices, short_period=12, long_period=26):
        """
        Calculate PPO values based on close prices.
        """
        close_prices = pd.Series(close_prices)

        # Calculate short-term EMA and long-term EMA
        ema_short = close_prices.ewm(span=short_period, adjust=False).mean()
        ema_long = close_prices.ewm(span=long_period, adjust=False).mean()

        # Calculate PPO
        ppo = ((ema_short - ema_long) / ema_long) * 100
        return ppo

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        # Validate data
        if not data:
            self.stdout.write("No data fetched from the database.")
            return

        self.stdout.write(f"Fetched {len(data)} data points.")

        symbols = [item["symbol"] for item in data]
        closes = [float(item["ltp"]) for item in data]
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if not (len(symbols) == len(closes) == len(timestamps)):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Calculate PPO values
            ppo_values = self.calculate_ppo(closes)

            # Skip NaN values (initial values for EMA calculation)
            for i in range(max(12, 26), len(ppo_values)):  # Use max of short and long period
                ppo = ppo_values.iloc[i]

                if pd.isna(ppo):
                    self.stdout.write(f"Skipping {symbols[i]} - PPO is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Signal determination
                signal = "Buy" if ppo > 0 else "Sell" if ppo < 0 else "Neutral"

                # Save to database
                PPOModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "ppo_value": ppo,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - PPO: {ppo:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating PPO: {str(e)}")
