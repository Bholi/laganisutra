# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import BopModel
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate Balance of Power (BOP), and store it in the database'

#     def fetch_data(self, api_url):
#         """
#         Fetch data from the provided API URL and return open, high, low, and close prices.
#         """
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             self.stdout.write("Failed to fetch data from API.")
#             return []

#     def calculate_bop(self, open_price, high, low, close):
#         """
#         Calculate the Balance of Power (BOP) for each data point.
#         Avoid division by zero.
#         """
#         if high - low == 0:
#             return 0  # You can choose a different default value if necessary
#         else:
#             return (close - open_price) / (high - low)

#     def handle(self, *args, **kwargs):
#         # API URL (replace with your actual API URL)
#         api_url = "https://tvapi.volcussoft.com/api/livedata/"
#         data = self.fetch_data(api_url)

#         if data:
#             # Extract data from the API response, removing commas and converting to float
#             symbols = [item["symbol"] for item in data]
#             opens = [float(item["open"].replace(',', '')) for item in data]
#             highs = [float(item["high"].replace(',', '')) for item in data]
#             lows = [float(item["low"].replace(',', '')) for item in data]
#             closes = [float(item["ltp"].replace(',', '')) for item in data]
#             timestamps = [item["datetime"] for item in data]

#             # Calculate Balance of Power values
#             bop_values = [
#                 self.calculate_bop(opens[i], highs[i], lows[i], closes[i])
#                 for i in range(len(data))
#             ]

#             # Store data in the database
#             for i in range(len(bop_values)):
#                 bop_value = bop_values[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))

#                 # Determine signal
#                 signal = "Buy" if bop_value > 0 else "Sell"

#                 # Save to database
#                 BopModel.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "bop": bop_value,
#                         "signal": signal
#                     }
#                 )

#                 self.stdout.write(f"Saved {symbol} - BOP: {bop_value:.4f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate Balance of Power.")


import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import BopModel
from livedata.models import LiveFeedData
from django.db.models import Max


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Balance of Power (BOP), and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values('symbol', 'open', 'high', 'low', 'ltp', 'datetime')
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_bop(self, open_price, high, low, close):
        """
        Calculate the Balance of Power (BOP) for each data point.
        Avoid division by zero.
        """
        if high - low == 0:
            return 0  # You can choose a different default value if necessary
        else:
            return (close - open_price) / (high - low)

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract data from the fetched data
            symbols = [item["symbol"] for item in data]
            opens = [float(item["open"].replace(',', '')) for item in data]
            highs = [float(item["high"].replace(',', '')) for item in data]
            lows = [float(item["low"].replace(',', '')) for item in data]
            closes = [float(item["ltp"].replace(',', '')) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate Balance of Power values
            bop_values = [
                self.calculate_bop(opens[i], highs[i], lows[i], closes[i])
                for i in range(len(data))
            ]

            # Store data in the database
            for i in range(len(bop_values)):
                bop_value = bop_values[i]
                symbol = symbols[i]
                timestamp = timestamps[i]
                
                # Determine signal
                signal = "Buy" if bop_value > 0 else "Sell"

                # Save to database
                BopModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date().isoformat(),
                    time=timestamp.time().isoformat(),
                    defaults={
                        "bop": bop_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - BOP: {bop_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate Balance of Power.")
