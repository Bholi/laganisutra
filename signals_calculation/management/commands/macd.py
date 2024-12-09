# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import MacdModel
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate MACD, and store it in the database'

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

#     def calculate_macd(self, close_prices, short_window=12, long_window=26, signal_window=9):
#         """
#         Calculate the MACD line, Signal line, and MACD Histogram.
#         """
#         close_prices = pd.Series(close_prices)
        
#         # Calculate the short and long exponential moving averages
#         short_ema = close_prices.ewm(span=short_window, adjust=False).mean()
#         long_ema = close_prices.ewm(span=long_window, adjust=False).mean()
        
#         # MACD Line
#         macd_line = short_ema - long_ema
        
#         # Signal Line
#         signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        
#         # MACD Histogram
#         macd_histogram = macd_line - signal_line
        
#         return macd_line, signal_line, macd_histogram

#     def handle(self, *args, **kwargs):
#         # API URL (replace with your actual API URL)
#         api_url = "https://tvapi.volcussoft.com/api/livedata/"
#         data = self.fetch_data(api_url)

#         if data:
#             close_prices = [float(item["ltp"]) for item in data]
#             symbols = [item["symbol"] for item in data]
#             timestamps = [item["datetime"] for item in data]
            
#             # Calculate MACD components
#             macd_line, signal_line, macd_histogram = self.calculate_macd(close_prices)
            
#             # Determine signals and store in the database
#             for i in range(len(macd_line)):
#                 macd_val = macd_line.iloc[i]
#                 signal_val = signal_line.iloc[i]
#                 hist_val = macd_histogram.iloc[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))
                
#                 # Determine signal
#                 if macd_val > signal_val:
#                     signal = "Buy"
#                 elif macd_val < signal_val:
#                     signal = "Sell"
#                 else:
#                     signal = "Hold"
                
#                 # Save to database
#                 MacdModel.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "macd_line": macd_val,
#                         "signal_line": signal_val,
#                         "macd_histogram": hist_val,
#                         "signal": signal
#                     }
#                 )
                
#                 self.stdout.write(f"Saved {symbol} - MACD Line: {macd_val:.2f}, Signal Line: {signal_val:.2f}, Histogram: {hist_val:.2f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate MACD.")



import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import MacdModel  # Assuming MacdModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate MACD, and store it in the database'

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

    def calculate_macd(self, close_prices, short_window=12, long_window=26, signal_window=9):
        """
        Calculate the MACD line, Signal line, and MACD Histogram.
        """
        close_prices = pd.Series(close_prices)
        
        # Calculate the short and long exponential moving averages
        short_ema = close_prices.ewm(span=short_window, adjust=False).mean()
        long_ema = close_prices.ewm(span=long_window, adjust=False).mean()
        
        # MACD Line
        macd_line = short_ema - long_ema
        
        # Signal Line
        signal_line = macd_line.ewm(span=signal_window, adjust=False).mean()
        
        # MACD Histogram
        macd_histogram = macd_line - signal_line
        
        return macd_line, signal_line, macd_histogram

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            close_prices = [float(item["ltp"]) for item in data]
            symbols = [item["symbol"] for item in data]
            timestamps = [item["datetime"] for item in data]
            
            # Calculate MACD components
            macd_line, signal_line, macd_histogram = self.calculate_macd(close_prices)
            
            # Determine signals and store in the database
            for i in range(len(macd_line)):
                macd_val = macd_line.iloc[i]
                signal_val = signal_line.iloc[i]
                hist_val = macd_histogram.iloc[i]
                symbol = symbols[i]
                timestamp = timestamps[i]
                
                # Determine signal
                if macd_val > signal_val:
                    signal = "Buy"
                elif macd_val < signal_val:
                    signal = "Sell"
                else:
                    signal = "Hold"
                
                # Save to database
                MacdModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "macd_line": macd_val,
                        "signal_line": signal_val,
                        "macd_histogram": hist_val,
                        "signal": signal
                    }
                )
                
                self.stdout.write(f"Saved {symbol} - MACD Line: {macd_val:.2f}, Signal Line: {signal_val:.2f}, Histogram: {hist_val:.2f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate MACD.")
