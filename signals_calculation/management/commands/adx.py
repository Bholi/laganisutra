# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import AdxModel
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate ADX, and store it in the database'

#     def fetch_data(self, api_url):
#         """
#         Fetch data from the provided API URL and return open, high, low, close prices.
#         """
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             self.stdout.write("Failed to fetch data from API.")
#             return []

#     def calculate_adx(self, high_prices, low_prices, close_prices, period=14):
#         """
#         Calculate the ADX value based on the high, low, and close prices.
#         """
#         plus_dm = []
#         minus_dm = []
#         tr = []

#         for i in range(1, len(high_prices)):
#             high_diff = high_prices[i] - high_prices[i - 1]
#             low_diff = low_prices[i - 1] - low_prices[i]

#             plus_dm.append(max(0, high_diff) if high_diff > low_diff else 0)
#             minus_dm.append(max(0, low_diff) if low_diff > high_diff else 0)
#             tr.append(max(high_prices[i] - low_prices[i], abs(high_prices[i] - close_prices[i - 1]), abs(low_prices[i] - close_prices[i - 1])))

#         # Smooth the values over the given period
#         plus_dm = pd.Series(plus_dm).rolling(window=period).sum()
#         minus_dm = pd.Series(minus_dm).rolling(window=period).sum()
#         tr = pd.Series(tr).rolling(window=period).sum()

#         # Calculate +DI and -DI
#         plus_di = (plus_dm / tr) * 100
#         minus_di = (minus_dm / tr) * 100

#         # Calculate ADX (using the smoothed +DI and -DI)
#         adx = pd.Series(abs(plus_di - minus_di) / (plus_di + minus_di) * 100).rolling(window=period).mean()

#         # Return the entire ADX series
#         return adx

#     def handle(self, *args, **kwargs):
#         # API URL (replace with your actual API URL)
#         api_url = "https://tvapi.volcussoft.com/api/livedata/"
#         data = self.fetch_data(api_url)

#         if data:
#             # Extract data from the API response
#             symbols = [item["symbol"] for item in data]
#             highs = [float(item["high"].replace(',', '')) for item in data]
#             lows = [float(item["low"].replace(',', '')) for item in data]
#             closes = [float(item["ltp"].replace(',', '')) for item in data]
#             timestamps = [item["datetime"] for item in data]

#             # Calculate ADX values (returns a series of ADX values)
#             adx_values = self.calculate_adx(highs, lows, closes)

#             # Iterate through the ADX values (skip the first 14 as they are NaN due to the rolling window)
#             for i in range(14, len(adx_values)):
#                 adx_value = adx_values.iloc[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i + len(timestamps) - len(adx_values)].replace("Z", "+00:00"))

#                 # Determine signal (For example, if ADX is above a threshold, signal "Strong", else "Weak")
#                 signal = "Strong" if adx_value > 25 else "Weak"

#                 # Save to database
#                 AdxModel.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "adx_value": adx_value,
#                         "signal": signal
#                     }
#                 )

#                 self.stdout.write(f"Saved {symbol} - ADX: {adx_value:.4f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate ADX.")


import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import AdxModel  # Assuming AdxModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate ADX, and store it in the database'

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

    def calculate_adx(self, high_prices, low_prices, close_prices, period=14):
        """
        Calculate the ADX value based on the high, low, and close prices.
        """
        plus_dm = []
        minus_dm = []
        tr = []

        for i in range(1, len(high_prices)):
            high_diff = high_prices[i] - high_prices[i - 1]
            low_diff = low_prices[i - 1] - low_prices[i]

            plus_dm.append(max(0, high_diff) if high_diff > low_diff else 0)
            minus_dm.append(max(0, low_diff) if low_diff > high_diff else 0)
            tr.append(max(high_prices[i] - low_prices[i], abs(high_prices[i] - close_prices[i - 1]), abs(low_prices[i] - close_prices[i - 1])))

        # Smooth the values over the given period
        plus_dm = pd.Series(plus_dm).rolling(window=period).sum()
        minus_dm = pd.Series(minus_dm).rolling(window=period).sum()
        tr = pd.Series(tr).rolling(window=period).sum()

        # Calculate +DI and -DI
        plus_di = (plus_dm / tr) * 100
        minus_di = (minus_dm / tr) * 100

        # Calculate ADX (using the smoothed +DI and -DI)
        adx = pd.Series(abs(plus_di - minus_di) / (plus_di + minus_di) * 100).rolling(window=period).mean()

        # Return the entire ADX series
        return adx

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

            # Calculate ADX values
            adx_values = self.calculate_adx(highs, lows, closes)

            # Skip the first 14 values (due to NaN from rolling window)
            for i in range(14, len(adx_values)):
                adx_value = adx_values.iloc[i]
                if pd.isna(adx_value):  # Skip if ADX is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - ADX is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Strong" if adx_value > 25 else "Weak"

                # Save to database
                AdxModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "adx_value": adx_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - ADX: {adx_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate ADX.")
