# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import CciData
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate CCI, and store it in the database'

#     def fetch_data(self, api_url):
#         """
#         Fetch data from the provided API URL and return it as a list of high, low, close prices.
#         """
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             self.stdout.write("Failed to fetch data from API.")
#             return []

#     def calculate_cci(self, high_prices, low_prices, close_prices, window=14):
#         """
#         Calculate the Commodity Channel Index (CCI) for the given high, low, and close prices.
#         """
#         # Calculate the typical price
#         typical_price = (high_prices + low_prices + close_prices) / 3
        
#         # Calculate the Simple Moving Average (SMA) of the typical price
#         sma = typical_price.rolling(window=window, min_periods=1).mean()
        
#         # Calculate the mean deviation
#         mean_deviation = typical_price.rolling(window=window, min_periods=1).apply(lambda x: (x - x.mean()).abs().mean())
        
#         # Calculate the CCI
#         cci = (typical_price - sma) / (0.015 * mean_deviation)
#         return cci

#     def handle(self, *args, **kwargs):
#         # API URL (replace with your actual API URL)
#         api_url = "https://tvapi.volcussoft.com/api/livedata/"
#         data = self.fetch_data(api_url)

#         if data:
#             high_prices = [float(item["high"]) for item in data]
#             low_prices = [float(item["low"]) for item in data]
#             close_prices = [float(item["ltp"]) for item in data]  # Assuming ltp is the close price
#             symbols = [item["symbol"] for item in data]
#             timestamps = [item["datetime"] for item in data]
            
#             # Convert the data into a Pandas DataFrame for easier manipulation
#             df = pd.DataFrame({
#                 'high': high_prices,
#                 'low': low_prices,
#                 'close': close_prices
#             })
            
#             # Calculate CCI
#             cci_values = self.calculate_cci(df['high'], df['low'], df['close'])
            
#             # Determine signals and store in the database
#             for i in range(len(cci_values)):
#                 cci_value = cci_values.iloc[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))
                
#                 # Determine signal
#                 if cci_value > 100:
#                     signal = "Buy"
#                 elif cci_value < -100:
#                     signal = "Sell"
#                 else:
#                     signal = "Hold"
                
#                 # Save to database
#                 CciData.objects.update_or_create(
#                     script_name=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "high": high_prices[i],
#                         "low": low_prices[i],
#                         "close": close_prices[i],
#                         "cci": cci_value,
#                         "signal": signal
#                     }
#                 )
                
#                 self.stdout.write(f"Saved {symbol} - CCI: {cci_value:.2f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate CCI.")


import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import CciData
from livedata.models import LiveFeedData
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate CCI, and store it in the database'

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

    def calculate_cci(self, high_prices, low_prices, close_prices, window=14):
        """
        Calculate the Commodity Channel Index (CCI) for the given high, low, and close prices.
        """
        # Calculate the typical price
        typical_price = (high_prices + low_prices + close_prices) / 3
        
        # Calculate the Simple Moving Average (SMA) of the typical price
        sma = typical_price.rolling(window=window, min_periods=1).mean()
        
        # Calculate the mean deviation
        mean_deviation = typical_price.rolling(window=window, min_periods=1).apply(lambda x: (x - x.mean()).abs().mean())
        
        # Calculate the CCI
        cci = (typical_price - sma) / (0.015 * mean_deviation)
        return cci

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            high_prices = [float(item["high"]) for item in data]
            low_prices = [float(item["low"]) for item in data]
            close_prices = [float(item["ltp"]) for item in data]  # Assuming ltp is the close price
            symbols = [item["symbol"] for item in data]
            timestamps = [item["datetime"] for item in data]
            
            # Convert the data into a Pandas DataFrame for easier manipulation
            df = pd.DataFrame({
                'high': high_prices,
                'low': low_prices,
                'close': close_prices
            })
            
            # Calculate CCI
            cci_values = self.calculate_cci(df['high'], df['low'], df['close'])
            
            # Determine signals and store in the database
            for i in range(len(cci_values)):
                cci_value = cci_values.iloc[i]
                if pd.isna(cci_value):
                    self.stdout.write(f"Skipping {symbols[i]} - CCI is Nan")
                    continue
                symbol = symbols[i]
                timestamp = timestamps[i]
                
                # Determine signal
                if cci_value > 100:
                    signal = "Buy"
                elif cci_value < -100:
                    signal = "Sell"
                else:
                    signal = "Hold"
                
                # Save to database
                CciData.objects.update_or_create(
                    script_name=symbol,
                    date=timestamp.date().isoformat(),
                    time=timestamp.time().isoformat(),
                    defaults={
                        "high": high_prices[i],
                        "low": low_prices[i],
                        "close": close_prices[i],
                        "cci": cci_value,
                        "signal": signal
                    }
                )
                
                self.stdout.write(f"Saved {symbol} - CCI: {cci_value:.2f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate CCI.")
