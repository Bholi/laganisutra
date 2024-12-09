# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import StochasticRSI
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate Stochastic RSI, and store it in the database'

#     def fetch_data(self, api_url):
#         """
#         Fetch data from the provided API URL and return it as a list of close prices.
#         """
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             self.stdout.write("Failed to fetch data from API.")
#             return []

#     def calculate_rsi(self, close_prices, period=14):
#         """
#         Calculate RSI values for the given close prices.
#         """
#         delta = close_prices.diff()
#         gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
#         loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
#         rs = gain / loss
#         rsi = 100 - (100 / (1 + rs))
#         return rsi

#     def calculate_stochrsi(self, rsi_values, period=14, k_period=3, d_period=3):
#         """
#         Calculate the Stochastic RSI %K and %D lines.
#         """
#         stochrsi_k = ((rsi_values - rsi_values.rolling(window=period).min()) /
#                       (rsi_values.rolling(window=period).max() - rsi_values.rolling(window=period).min())) * 100
#         stochrsi_d = stochrsi_k.rolling(window=d_period).mean()
#         return stochrsi_k, stochrsi_d

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

#             # Calculate RSI values
#             rsi_values = self.calculate_rsi(df['close'])
            
#             # Calculate Stochastic RSI %K and %D
#             stochrsi_k, stochrsi_d = self.calculate_stochrsi(rsi_values)

#             # Determine signals and store in the database
#             for i in range(len(stochrsi_k)):
#                 k_value = stochrsi_k.iloc[i]
#                 d_value = stochrsi_d.iloc[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))

#                 # Determine signal
#                 if i > 0:
#                     prev_k = stochrsi_k.iloc[i - 1]
#                     prev_d = stochrsi_d.iloc[i - 1]
#                     if k_value > d_value and prev_k <= prev_d:
#                         signal = "Buy"
#                     elif k_value < d_value and prev_k >= prev_d:
#                         signal = "Sell"
#                     else:
#                         signal = "Hold"
#                 else:
#                     signal = "Hold"

#                 # Save to database
#                 StochasticRSI.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "close_price": close_prices[i],
#                         "stochrsi_k": k_value,
#                         "stochrsi_d": d_value,
#                         "signal": signal
#                     }
#                 )

#                 self.stdout.write(f"Saved {symbol} - Stochastic RSI %K: {k_value:.2f}, %D: {d_value:.2f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate Stochastic RSI.")

import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import StochasticRSI
from livedata.models import LiveFeedData
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Stochastic RSI, and store it in the database'

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

    def calculate_rsi(self, close_prices, period=14):
        """
        Calculate RSI values for the given close prices.
        """
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def calculate_stochrsi(self, rsi_values, period=14, k_period=3, d_period=3):
        """
        Calculate the Stochastic RSI %K and %D lines.
        """
        stochrsi_k = ((rsi_values - rsi_values.rolling(window=period).min()) /
                      (rsi_values.rolling(window=period).max() - rsi_values.rolling(window=period).min())) * 100
        stochrsi_d = stochrsi_k.rolling(window=d_period).mean()
        return stochrsi_k, stochrsi_d

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

            # Calculate RSI values
            rsi_values = self.calculate_rsi(df['close'])
            
            # Calculate Stochastic RSI %K and %D
            stochrsi_k, stochrsi_d = self.calculate_stochrsi(rsi_values)

            # Determine signals and store in the database
            for i in range(len(stochrsi_k)):
                k_value = stochrsi_k.iloc[i]
                d_value = stochrsi_d.iloc[i]
                if pd.isna(k_value) or pd.isna(d_value):
                    self.stdout.write(f"Skipping {symbols[i]} - StochasticRsi is NaN")
                    continue
                symbol = symbols[i]
                timestamp = timestamps[i]
                
                # Determine signal
                if i > 0:
                    prev_k = stochrsi_k.iloc[i - 1]
                    prev_d = stochrsi_d.iloc[i - 1]
                    if k_value > d_value and prev_k <= prev_d:
                        signal = "Buy"
                    elif k_value < d_value and prev_k >= prev_d:
                        signal = "Sell"
                    else:
                        signal = "Hold"
                else:
                    signal = "Hold"

                # Save to database
                StochasticRSI.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date().isoformat(),
                    time=timestamp.time().isoformat(),
                    defaults={
                        "close_price": close_prices[i],
                        "stochrsi_k": k_value,
                        "stochrsi_d": d_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - Stochastic RSI %K: {k_value:.2f}, %D: {d_value:.2f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Stochastic RSI.")
