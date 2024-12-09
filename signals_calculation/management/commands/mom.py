# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import MomentumIndicator
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate Momentum, and store it in the database'

#     def fetch_data(self, api_url):
#         """
#         Fetch data from the provided API URL and return it as a list of close prices.
#         """
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             self.stdout.write("Failed to fetch data from API.")
#             return []

#     def calculate_momentum(self, close_prices, period=10):
#         """
#         Calculate the Momentum Indicator for the given close prices.
#         Momentum is calculated as the difference between the current close and the close 'period' days ago.
#         """
#         momentum = close_prices.diff(period)
#         return momentum

#     def handle(self, *args, **kwargs):
#         # API URL (replace with your actual API URL)
#         api_url = "https://tvapi.volcussoft.com/api/livedata/"
#         data = self.fetch_data(api_url)

#         if data:
#             close_prices = [float(item["ltp"]) for item in data]
#             symbols = [item["symbol"] for item in data]
#             timestamps = [item["datetime"] for item in data]
            
#             # Convert the data into a Pandas DataFrame for easier manipulation
#             df = pd.DataFrame({
#                 'close': close_prices
#             })
            
#             # Calculate Momentum
#             momentum_values = self.calculate_momentum(df['close'])
            
#             # Determine signals and store in the database
#             for i in range(len(momentum_values)):
#                 mom_value = momentum_values.iloc[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))
                
#                 # Determine signal based on Momentum change
#                 if mom_value > 0:
#                     signal = "Buy" if mom_value > momentum_values.iloc[i - 1] else "Hold"
#                 elif mom_value < 0:
#                     signal = "Sell" if mom_value < momentum_values.iloc[i - 1] else "Hold"
#                 else:
#                     signal = "Hold"
                
#                 # Save to database
#                 MomentumIndicator.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "close_price": close_prices[i],
#                         "mom_value": mom_value,
#                         "signal": signal
#                     }
#                 )
                
#                 self.stdout.write(f"Saved {symbol} - Momentum: {mom_value:.2f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate Momentum.")

import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import MomentumIndicator
from livedata.models import LiveFeedData
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Momentum, and store it in the database'

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

    def calculate_momentum(self, close_prices, period=10):
        """
        Calculate the Momentum Indicator for the given close prices.
        Momentum is calculated as the difference between the current close and the close 'period' days ago.
        """
        momentum = close_prices.diff(period)
        return momentum

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            close_prices = [float(item["ltp"]) for item in data]
            symbols = [item["symbol"] for item in data]
            timestamps = [item["datetime"] for item in data]
            
            # Convert the data into a Pandas DataFrame for easier manipulation
            df = pd.DataFrame({
                'close': close_prices
            })
            
            # Calculate Momentum
            momentum_values = self.calculate_momentum(df['close'])
            
            # Determine signals and store in the database
            for i in range(len(momentum_values)):
                mom_value = momentum_values.iloc[i]
                if pd.isna(mom_value):
                    self.stdout.write(f"Skipping {symbols[i]} - MOM is Nan")
                    continue
                symbol = symbols[i]
                timestamp = timestamps[i]
                
                # Determine signal based on Momentum change
                if mom_value > 0:
                    signal = "Buy" if mom_value > momentum_values.iloc[i - 1] else "Hold"
                elif mom_value < 0:
                    signal = "Sell" if mom_value < momentum_values.iloc[i - 1] else "Hold"
                else:
                    signal = "Hold"
                
                # Save to database
                MomentumIndicator.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date().isoformat(),
                    time=timestamp.time().isoformat(),
                    defaults={
                        "close_price": close_prices[i],
                        "mom_value": mom_value,
                        "signal": signal
                    }
                )
                
                self.stdout.write(f"Saved {symbol} - Momentum: {mom_value:.2f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Momentum.")
