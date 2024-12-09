import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import FisherModel  # Assuming FisherModel exists for storing the results
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime
import numpy as np


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Fisher Transform, and store it in the database'

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

    def calculate_fisher_transform(self, high_prices, low_prices, period=9):
        """
        Calculate the Fisher Transform values based on high and low prices.
        """
        # Calculate the midpoint values (X)
        mid_point = (pd.Series(high_prices) + pd.Series(low_prices)) / 2

        # Calculate the highest high and the lowest low over the period
        high_max = pd.Series(high_prices).rolling(window=period).max()
        low_min = pd.Series(low_prices).rolling(window=period).min()

        # Normalize the price (X)
        value = 2 * ((mid_point - low_min) / (high_max - low_min) - 0.5)
        
        # Fisher Transform calculation
        fisher = 0.5 * (pd.Series(value).apply(lambda x: np.log(1 + x) - np.log(1 - x)))
        
        # Apply a smoothing function to the Fisher Transform (EMA)
        fisher_smoothed = fisher.ewm(span=period, adjust=False).mean()

        return fisher_smoothed

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

            # Calculate Fisher Transform
            fisher_smoothed = self.calculate_fisher_transform(highs, lows)

            # Iterate through the data to determine signals and save them
            for i in range(len(fisher_smoothed)):
                fisher_value = fisher_smoothed.iloc[i]
                if pd.isna(fisher_value):  # Skip if CFO is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - Fisher is NaN")
                    continue
                # Determine the signal based on the Fisher Transform
                if fisher_value > 0:
                    signal = "Buy"
                elif fisher_value < 0:
                    signal = "Sell"
                else:
                    signal = "Neutral"

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Save to the database
                FisherModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "fisher_transform": fisher_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - Fisher Transform: {fisher_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Fisher Transform.")
