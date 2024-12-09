# import requests
# import pandas as pd
# from django.core.management.base import BaseCommand
# from momentum.models import AwesomeOscillator
# from datetime import datetime

# class Command(BaseCommand):
#     help = 'Fetch data from API, calculate AO, and store it in the database'

#     def fetch_data(self, api_url):
#         """
#         Fetch data from the provided API URL and return it as a list of high and low prices.
#         """
#         response = requests.get(api_url)
#         if response.status_code == 200:
#             data = response.json()
#             return data
#         else:
#             self.stdout.write("Failed to fetch data from API.")
#             return []

#     def calculate_ao(self, high_prices, low_prices, short_period=5, long_period=34):
#         """
#         Calculate the Awesome Oscillator (AO) for the given high and low prices.
#         AO is the difference between the 5-period and 34-period SMA of the midpoint price.
#         """
#         # Calculate midpoint price
#         midpoint_price = (high_prices + low_prices) / 2
        
#         # Calculate short and long SMAs
#         short_sma = midpoint_price.rolling(window=short_period, min_periods=1).mean()
#         long_sma = midpoint_price.rolling(window=long_period, min_periods=1).mean()
        
#         # Calculate AO
#         ao = short_sma - long_sma
#         return ao

#     def handle(self, *args, **kwargs):
#         # API URL (replace with your actual API URL)
#         api_url = "https://tvapi.volcussoft.com/api/livedata/"
#         data = self.fetch_data(api_url)

#         if data:
#             high_prices = [float(item["high"]) for item in data]
#             low_prices = [float(item["low"]) for item in data]
#             symbols = [item["symbol"] for item in data]
#             timestamps = [item["datetime"] for item in data]
            
#             # Convert the data into a Pandas DataFrame for easier manipulation
#             df = pd.DataFrame({
#                 'high': high_prices,
#                 'low': low_prices,
#             })
            
#             # Calculate AO
#             ao_values = self.calculate_ao(df['high'], df['low'])
            
#             # Determine signals and store in the database
#             previous_ao = None
#             for i in range(len(ao_values)):
#                 ao_value = ao_values.iloc[i]
#                 symbol = symbols[i]
#                 timestamp = datetime.fromisoformat(timestamps[i].replace("Z", "+00:00"))
                
#                 # Determine signal based on AO change
#                 if previous_ao is not None:
#                     if ao_value > 0 and previous_ao <= 0:
#                         signal = "Buy"
#                     elif ao_value < 0 and previous_ao >= 0:
#                         signal = "Sell"
#                     else:
#                         signal = "Hold"
#                 else:
#                     signal = "Hold"
                
#                 previous_ao = ao_value  # Update previous AO for the next iteration
                
#                 # Save to database
#                 AwesomeOscillator.objects.update_or_create(
#                     script_name=symbol,
#                     date=timestamp.date().isoformat(),
#                     time=timestamp.time().isoformat(),
#                     defaults={
#                         "high": high_prices[i],
#                         "low": low_prices[i],
#                         "ao_value": ao_value,
#                         "signal": signal
#                     }
#                 )
                
#                 self.stdout.write(f"Saved {symbol} - AO: {ao_value:.2f}, Signal: {signal}")
#         else:
#             self.stdout.write("No data to calculate AO.")


import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import AwesomeOscillator
from livedata.models import LiveFeedData
from datetime import datetime
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate AO, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        # Get the latest datetime
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values('symbol', 'high', 'low', 'datetime')
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_ao(self, high_prices, low_prices, short_period=5, long_period=34):
        """
        Calculate the Awesome Oscillator (AO) for the given high and low prices.
        AO is the difference between the 5-period and 34-period SMA of the midpoint price.
        """
        # Calculate midpoint price
        midpoint_price = (high_prices + low_prices) / 2
        
        # Calculate short and long SMAs
        short_sma = midpoint_price.rolling(window=short_period, min_periods=1).mean()
        long_sma = midpoint_price.rolling(window=long_period, min_periods=1).mean()
        
        # Calculate AO
        ao = short_sma - long_sma
        return ao

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            high_prices = [float(item["high"]) for item in data]
            low_prices = [float(item["low"]) for item in data]
            symbols = [item["symbol"] for item in data]
            timestamps = [item["datetime"] for item in data]
            
            # Convert the data into a Pandas DataFrame for easier manipulation
            df = pd.DataFrame({
                'high': high_prices,
                'low': low_prices,
            })
            
            # Calculate AO
            ao_values = self.calculate_ao(df['high'], df['low'])
            
            # Determine signals and store in the database
            previous_ao = None
            for i in range(len(ao_values)):
                ao_value = ao_values.iloc[i]
                symbol = symbols[i]
                timestamp = timestamps[i]
                
                # Determine signal based on AO change
                if previous_ao is not None:
                    if ao_value > 0 and previous_ao <= 0:
                        signal = "Buy"
                    elif ao_value < 0 and previous_ao >= 0:
                        signal = "Sell"
                    else:
                        signal = "Hold"
                else:
                    signal = "Hold"
                
                previous_ao = ao_value  # Update previous AO for the next iteration
                
                # Save to database
                AwesomeOscillator.objects.update_or_create(
                    script_name=symbol,
                    date=timestamp.date().isoformat(),
                    time=timestamp.time().isoformat(),
                    defaults={
                        "high": high_prices[i],
                        "low": low_prices[i],
                        "ao_value": ao_value,
                        "signal": signal
                    }
                )
                
                self.stdout.write(f"Saved {symbol} - AO: {ao_value:.2f}, Signal: {signal}")
        else:
            self.stdout.write("No data to calculate AO.")
