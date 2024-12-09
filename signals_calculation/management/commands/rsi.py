# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import RsiModel
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate RSI, and store it in the database'

#     def fetch_data(self, api_url):
#         """
#         Fetch data from the provided API URL and return it as a list of closing prices.
#         """
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             self.stdout.write("Failed to fetch data from API.")
#             return []

#     def calculate_rsi(self, close_prices, window=14):
#         """
#         Calculate the Relative Strength Index (RSI) for a list of close prices.
#         """
#         close_prices = pd.Series(close_prices)
#         delta = close_prices.diff()
#         gains = delta.where(delta > 0, 0)
#         losses = -delta.where(delta < 0, 0)
#         avg_gain = gains.rolling(window=window, min_periods=1).mean()
#         avg_loss = losses.rolling(window=window, min_periods=1).mean()
#         rs = avg_gain / avg_loss
#         rsi = 100 - (100 / (1 + rs))
#         return rsi

#     def handle(self, *args, **kwargs):
#         # API URL (replace with your actual API URL)
#         api_url = "https://tvapi.volcussoft.com/api/livedata/"
#         data = self.fetch_data(api_url)

#         if data:
#             close_prices = [float(item["ltp"]) for item in data]
#             symbols = [item["symbol"] for item in data]
#             timestamps = [item["datetime"] for item in data]
            
#             # Calculate RSI
#             rsi_values = self.calculate_rsi(close_prices, window=14)
            
#             # Determine signals and store in the database
#             for i in range(len(rsi_values)):
#                 rsi_value = rsi_values.iloc[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))
                
#                 # Determine signal
#                 if rsi_value < 30:
#                     signal = "Buy"
#                 elif rsi_value > 70:
#                     signal = "Sell"
#                 else:
#                     signal = "Hold"
                
#                 # Save to database
#                 RsiModel.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "rsi_value": rsi_value,
#                         "signal": signal
#                     }
#                 )
                
#                 self.stdout.write(f"Saved {symbol} - RSI: {rsi_value:.2f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate RSI.")

import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import RsiModel
from livedata.models import LiveFeedData

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate RSI, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values('symbol', 'ltp', 'datetime')
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_rsi(self, close_prices, window=14):
        """
        Calculate the Relative Strength Index (RSI) for a list of close prices.
        """
        close_prices = pd.Series(close_prices)
        delta = close_prices.diff()
        gains = delta.where(delta > 0, 0)
        losses = -delta.where(delta < 0, 0)
        avg_gain = gains.rolling(window=window, min_periods=1).mean()
        avg_loss = losses.rolling(window=window, min_periods=1).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            close_prices = [float(item["ltp"]) for item in data]
            symbols = [item["symbol"] for item in data]
            timestamps = [item["datetime"] for item in data]
            
            # Calculate RSI
            rsi_values = self.calculate_rsi(close_prices, window=14)
            
            # Determine signals and store in the database
            for i in range(len(rsi_values)):
                rsi_value = rsi_values.iloc[i]
                if pd.isna(rsi_value):
                    self.stdout.write(f"Skipping {symbols[i]} - RSI is Nan")
                    continue
                symbol = symbols[i]
                timestamp = timestamps[i]
                
                # Determine signal
                if rsi_value < 30:
                    signal = "Buy"
                elif rsi_value > 70:
                    signal = "Sell"
                else:
                    signal = "Hold"
                
                # Save to database
                RsiModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "rsi_value": rsi_value,
                        "signal": signal
                    }
                )
                
                self.stdout.write(f"Saved {symbol} - RSI: {rsi_value:.2f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate RSI.")
