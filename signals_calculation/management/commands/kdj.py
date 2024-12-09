import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import KDJModel  # Assuming KdjModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate KDJ, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol', 'high', 'low', 'ltp', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_kdj(self, high_prices, low_prices, close_prices, period=14):
        """
        Calculate the KDJ values based on high, low, and close prices.
        """
        high_prices = pd.Series(high_prices)
        low_prices = pd.Series(low_prices)
        close_prices = pd.Series(close_prices)

        # Calculate the %K line
        low_min = low_prices.rolling(window=period).min()
        high_max = high_prices.rolling(window=period).max()
        k = ((close_prices - low_min) / (high_max - low_min)) * 100

        # Calculate the %D line (3-period moving average of %K)
        d = k.rolling(window=3).mean()

        # Calculate the %J line
        j = (3 * k) - (2 * d)

        return k, d, j

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

            # Calculate KDJ values
            k_values, d_values, j_values = self.calculate_kdj(highs, lows, closes)

            # Skip the first 'period' values (due to NaN from rolling window)
            period = 14
            for i in range(period, len(k_values)):
                k = k_values.iloc[i]
                d = d_values.iloc[i]
                j = j_values.iloc[i]

                if pd.isna(k) or pd.isna(d) or pd.isna(j):  # Skip if any value is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - K/D/J has NaN values")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                if j > k > d:
                    signal = "Buy"
                elif j < k < d:
                    signal = "Sell"
                else:
                    signal = "Neutral"

                # Save to database
                KDJModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "k_value": k,
                        "d_value": d,
                        "j_value": j,
                        "signal": signal
                    }
                )

                self.stdout.write(
                    f"Saved {symbol} - K: {k:.2f}, D: {d:.2f}, J: {j:.2f}, Signal: {signal}"
                )
        else:
            self.stdout.write("No data to calculate KDJ.")
