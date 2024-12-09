# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import WilliamPercentR
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate Williams %R, and store it in the database'

#     def fetch_data(self, api_url):
#         """
#         Fetch data from the provided API URL and return high, low, and close prices.
#         """
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             self.stdout.write("Failed to fetch data from API.")
#             return []

#     def calculate_willr(self, high, low, close, period=14):
#         """
#         Calculate Williams %R for the given high, low, and close prices.
#         """
#         highest_high = high.rolling(window=period).max()
#         lowest_low = low.rolling(window=period).min()
#         willr = ((highest_high - close) / (highest_high - lowest_low)) * -100
#         return willr

#     def handle(self, *args, **kwargs):
#         # API URL (replace with your actual API URL)
#         api_url = "https://tvapi.volcussoft.com/api/livedata/"
#         data = self.fetch_data(api_url)

#         if data:
#             highs = [float(item["high"]) for item in data]
#             lows = [float(item["low"]) for item in data]
#             closes = [float(item["ltp"]) for item in data]
#             symbols = [item["symbol"] for item in data]
#             timestamps = [item["datetime"] for item in data]

#             # Convert data into a Pandas DataFrame for easier manipulation
#             df = pd.DataFrame({
#                 'high': highs,
#                 'low': lows,
#                 'close': closes
#             })

#             # Calculate Williams %R values
#             willr_values = self.calculate_willr(df['high'], df['low'], df['close'])

#             # Determine signals and store in the database
#             for i in range(len(willr_values)):
#                 willr_value = willr_values.iloc[i]
#                 symbol = symbols[i]
#                 high = highs[i]
#                 low = lows[i]
#                 close = closes[i]
#                 timestamp = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))

#                 # Determine signal
#                 if willr_value > -80:
#                     signal = "Buy"
#                 elif willr_value < -20:
#                     signal = "Sell"
#                 else:
#                     signal = "Hold"

#                 # Save to database
#                 WilliamPercentR.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "high": high,
#                         "low": low,
#                         "close": close,
#                         "willr_value": willr_value,
#                         "signal": signal
#                     }
#                 )

#                 self.stdout.write(f"Saved {symbol} - Williams %R: {willr_value:.2f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate Williams %R.")


# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import WilliamPercentR
# from livedata.models import LiveFeedData
# from django.db.models import Max

# class Command(BaseCommand):
#     help = 'Fetch data from DB, calculate Williams %R, and store it in the database'

#     def fetch_data_from_db(self):
#         """
#         Fetch the latest data from the database based on the datetime field.
#         """
#         # Get the latest datetime
#         latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
#         # Fetch data with the latest datetime
#         if latest_datetime:
#             data = LiveFeedData.objects.filter(datetime=latest_datetime).values('symbol', 'high', 'low', 'ltp', 'datetime')
#             return list(data)
#         else:
#             self.stdout.write("No data found in the database.")
#             return []

#     def calculate_willr(self, high, low, close, period=14):
#         """
#         Calculate Williams %R for the given high, low, and close prices.
#         """
#         highest_high = high.rolling(window=period).max()
#         lowest_low = low.rolling(window=period).min()
#         willr = ((highest_high - close) / (highest_high - lowest_low)) * -100
#         return willr

#     def handle(self, *args, **kwargs):
#         # Fetch data from the database
#         data = self.fetch_data_from_db()

#         if data:
#             highs = [float(item["high"]) for item in data]
#             lows = [float(item["low"]) for item in data]
#             closes = [float(item["ltp"]) for item in data]
#             symbols = [item["symbol"] for item in data]
#             timestamps = [item["datetime"] for item in data]

#             # Convert data into a Pandas DataFrame for easier manipulation
#             df = pd.DataFrame({
#                 'high': highs,
#                 'low': lows,
#                 'close': closes
#             })

#             # Calculate Williams %R values
#             willr_values = self.calculate_willr(df['high'], df['low'], df['close'])

#             # Determine signals and store in the database
#             for i in range(len(willr_values)):
#                 willr_value = willr_values.iloc[i]
#                 if pd.isna(willr_value):
#                     self.stdout.write(f"Skipping {symbols[i]} - WILLR is Nan")
#                     continue
#                 symbol = symbols[i]
#                 high = highs[i]
#                 low = lows[i]
#                 close = closes[i]
#                 timestamp = timestamps[i]

#                 # Determine signal
#                 if willr_value > -80:
#                     signal = "Buy"
#                 elif willr_value < -20:
#                     signal = "Sell"
#                 else:
#                     signal = "Hold"

#                 # Save to database
#                 WilliamPercentR.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "high": high,
#                         "low": low,
#                         "close": close,
#                         "willr_value": willr_value,
#                         "signal": signal
#                     }
#                 )

#                 self.stdout.write(f"Saved {symbol} - Williams %R: {willr_value:.2f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate Williams %R.")

import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import WilliamPercentR  # Assuming WilliamPercentR exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Williams %R, and store it in the database'

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

    def calculate_williams_r(self, high_prices, low_prices, close_prices, period=14):
        """
        Calculate the Williams %R based on the high, low, and close prices.
        """
        williams_r = []
        for i in range(period - 1, len(close_prices)):
            highest_high = max(high_prices[i - period + 1:i + 1])
            lowest_low = min(low_prices[i - period + 1:i + 1])
            current_close = close_prices[i]

            # Calculate %R
            if highest_high - lowest_low == 0:  # Prevent division by zero
                williams_r.append(float('nan'))
            else:
                williams_r.append(((highest_high - current_close) / (highest_high - lowest_low)) * -100)

        # Pad initial values with NaN to align with the data length
        williams_r = [float('nan')] * (period - 1) + williams_r
        return pd.Series(williams_r)

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

            # Calculate Williams %R values
            williams_r_values = self.calculate_williams_r(highs, lows, closes)

            # Skip NaN values
            for i in range(len(williams_r_values)):
                williams_r_value = williams_r_values.iloc[i]
                if pd.isna(williams_r_value):  # Skip if Williams %R is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - Williams %R is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Buy" if williams_r_value < -80 else "Sell" if williams_r_value > -20 else "Neutral"

                # Save to database
                WilliamPercentR.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "willr_value": williams_r_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - Williams %R: {williams_r_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Williams %R.")
