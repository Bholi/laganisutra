# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import UltimateOscillator
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate Ultimate Oscillator (UO), and store it in the database'

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

#     def calculate_ultimate_oscillator(self, high, low, close, short_period=7, medium_period=14, long_period=28):
#         """
#         Calculate the Ultimate Oscillator (UO) for given high, low, and close prices.
#         """
#         # Calculate True Low, True Range, and Buying Pressure
#         tr_low = pd.DataFrame({'low': low, 'close_prev': close.shift(1)}).min(axis=1)
#         bp = close - tr_low
#         tr = pd.DataFrame({'high': high, 'low': low, 'close_prev': close.shift(1)}).apply(lambda row: row.max() - row.min(), axis=1)
        
#         # Calculate averages for different periods
#         avg7 = bp.rolling(window=short_period).sum() / tr.rolling(window=short_period).sum()
#         avg14 = bp.rolling(window=medium_period).sum() / tr.rolling(window=medium_period).sum()
#         avg28 = bp.rolling(window=long_period).sum() / tr.rolling(window=long_period).sum()
        
#         # Calculate Ultimate Oscillator
#         uo = 100 * ((4 * avg7) + (2 * avg14) + avg28) / 7
#         return uo

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

#             # Calculate Ultimate Oscillator values
#             uo_values = self.calculate_ultimate_oscillator(df['high'], df['low'], df['close'])

#             # Determine signals and store in the database
#             for i in range(len(uo_values)):
#                 uo_value = uo_values.iloc[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))

#                 # Determine signal
#                 if uo_value > 70:
#                     signal = "Sell"
#                 elif uo_value < 30:
#                     signal = "Buy"
#                 else:
#                     signal = "Hold"

#                 # Save to database
#                 UltimateOscillator.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "uo_value": uo_value,
#                         "signal": signal
#                     }
#                 )

#                 self.stdout.write(f"Saved {symbol} - UO: {uo_value:.2f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate Ultimate Oscillator.")


import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import UltimateOscillator
from livedata.models import LiveFeedData
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Ultimate Oscillator (UO), and store it in the database'

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

    def calculate_ultimate_oscillator(self, high, low, close, short_period=7, medium_period=14, long_period=28):
        """
        Calculate the Ultimate Oscillator (UO) for given high, low, and close prices.
        """
        # Calculate True Low, True Range, and Buying Pressure
        tr_low = pd.DataFrame({'low': low, 'close_prev': close.shift(1)}).min(axis=1)
        bp = close - tr_low
        tr = pd.DataFrame({'high': high, 'low': low, 'close_prev': close.shift(1)}).apply(lambda row: row.max() - row.min(), axis=1)
        
        # Calculate averages for different periods
        avg7 = bp.rolling(window=short_period).sum() / tr.rolling(window=short_period).sum()
        avg14 = bp.rolling(window=medium_period).sum() / tr.rolling(window=medium_period).sum()
        avg28 = bp.rolling(window=long_period).sum() / tr.rolling(window=long_period).sum()
        
        # Calculate Ultimate Oscillator
        uo = 100 * ((4 * avg7) + (2 * avg14) + avg28) / 7
        return uo

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            highs = [float(item["high"]) for item in data]
            lows = [float(item["low"]) for item in data]
            closes = [float(item["ltp"]) for item in data]
            symbols = [item["symbol"] for item in data]
            timestamps = [item["datetime"] for item in data]

            # Convert data into a Pandas DataFrame for easier manipulation
            df = pd.DataFrame({
                'high': highs,
                'low': lows,
                'close': closes
            })

            # Calculate Ultimate Oscillator values
            uo_values = self.calculate_ultimate_oscillator(df['high'], df['low'], df['close'])

            # Determine signals and store in the database
            for i in range(len(uo_values)):
                uo_value = uo_values.iloc[i]
                if pd.isna(uo_value):
                    self.stdout.write(f"Skipping {symbols[i]} - UO is Nan")
                    continue
                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                if uo_value > 70:
                    signal = "Sell"
                elif uo_value < 30:
                    signal = "Buy"
                else:
                    signal = "Hold"

                # Save to database
                UltimateOscillator.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date().isoformat(),
                    time=timestamp.time().isoformat(),
                    defaults={
                        "uo_value": uo_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - UO: {uo_value:.2f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Ultimate Oscillator.")
