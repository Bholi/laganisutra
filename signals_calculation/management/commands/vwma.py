# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import VwmaModel
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate VWMA, and store it in the database'

#     def fetch_data(self, api_url):
#         """
#         Fetch data from the provided API URL and return open, high, low, close, volume prices.
#         """
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             return response.json()
#         else:
#             self.stdout.write("Failed to fetch data from API.")
#             return []

#     def calculate_vwma(self, closes, volumes, period=14):
#         """
#         Calculate the Volume Weighted Moving Average (VWMA).
#         """
#         vwma_values = []
#         for i in range(len(closes) - period + 1):
#             weighted_prices = [closes[j] * volumes[j] for j in range(i, i + period)]
#             total_volume = sum(volumes[i:i + period])
#             vwma = sum(weighted_prices) / total_volume if total_volume != 0 else 0
#             vwma_values.append(vwma)
#         return vwma_values

#     def handle(self, *args, **kwargs):
#         # API URL (replace with your actual API URL)
#         api_url = "https://tvapi.volcussoft.com/api/livedata/"
#         data = self.fetch_data(api_url)

#         if data:
#             # Extract data from the API response, removing commas and converting to float
#             symbols = [item["symbol"] for item in data]
#             closes = [float(item["ltp"].replace(',', '')) for item in data]
#             volumes = [float(item["volume"].replace(',', '')) for item in data]
#             timestamps = [item["datetime"] for item in data]

#             # Calculate VWMA values
#             vwma_values = self.calculate_vwma(closes, volumes)

#             # Store data in the database
#             for i in range(len(vwma_values)):
#                 vwma_value = vwma_values[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i + len(timestamps) - len(vwma_values)].replace("Z", "+00:00"))

#                 # Determine signal (For example, if VWMA is rising, signal "Buy", else "Sell")
#                 signal = "Buy" if vwma_value > closes[i] else "Sell"

#                 # Save to database
#                 VwmaModel.objects.update_or_create(
#                     symbol=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "vwma_value": vwma_value,
#                         "signal": signal
#                     }
#                 )

#                 self.stdout.write(f"Saved {symbol} - VWMA: {vwma_value:.4f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate VWMA.")


import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import VwmaModel  # Assuming VwmaModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate VWMA, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values('symbol', 'ltp', 'volume', 'datetime')
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_vwma(self, prices, volumes, period=14):
        """
        Calculate VWMA based on prices and volumes.
        """
        vwma_values = []
        for i in range(period - 1, len(prices)):
            # Subset the prices and volumes for the given period
            price_subset = prices[i - period + 1:i + 1]
            volume_subset = volumes[i - period + 1:i + 1]

            # Calculate VWMA
            numerator = sum(p * v for p, v in zip(price_subset, volume_subset))
            denominator = sum(volume_subset)
            
            if denominator == 0:  # Prevent division by zero
                vwma_values.append(float('nan'))
            else:
                vwma_values.append(numerator / denominator)

        # Pad initial values with NaN to align with the data length
        vwma_values = [float('nan')] * (period - 1) + vwma_values
        return pd.Series(vwma_values)

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            prices = [float(item["ltp"]) for item in data]
            volumes = [float(item["volume"].replace(',','')) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate VWMA values
            vwma_values = self.calculate_vwma(prices, volumes)

            # Skip NaN values
            for i in range(len(vwma_values)):
                vwma_value = vwma_values.iloc[i]
                if pd.isna(vwma_value):  # Skip if VWMA is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - VWMA is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal (optional, based on VWMA trend)
                signal = "Buy" if i > 0 and vwma_values.iloc[i] > vwma_values.iloc[i - 1] else "Sell"

                # Save to database
                VwmaModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "vwma_value": vwma_value,
                        "signal": signal
                    }
                )

                self.stdout.write(f"Saved {symbol} - VWMA: {vwma_value:.4f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate VWMA.")
