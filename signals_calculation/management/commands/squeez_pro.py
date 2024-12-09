import pandas as pd
import numpy as np
from django.core.management.base import BaseCommand
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from momentum.models import  SqueezeProModel # Assuming SqueezeProModel exists for storing Squeeze Pro data
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Squeeze Pro, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch data from the database ordered by datetime.
        """
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol', 'high', 'low', 'ltp', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []
        

    def calculate_bollinger_bands(self, close_prices, period=20, std_dev_multiplier=2):
        """
        Calculate Bollinger Bands (Upper and Lower)
        """
        rolling_mean = pd.Series(close_prices).rolling(window=period).mean()
        rolling_std = pd.Series(close_prices).rolling(window=period).std()

        upper_band = rolling_mean + (rolling_std * std_dev_multiplier)
        lower_band = rolling_mean - (rolling_std * std_dev_multiplier)

        return upper_band, lower_band

    def calculate_keltner_channels(self, high_prices, low_prices, close_prices, period=20, atr_multiplier=1.5):
        """
        Calculate Keltner Channels (Upper and Lower)
        """
        # Calculate the Average True Range (ATR)
        tr = pd.Series([max(high - low, abs(high - close), abs(low - close)) for high, low, close in zip(high_prices, low_prices, close_prices)])
        atr = tr.rolling(window=period).mean()

        # Calculate the Keltner Channels
        rolling_mean = pd.Series(close_prices).rolling(window=period).mean()
        upper_kc = rolling_mean + (atr * atr_multiplier)
        lower_kc = rolling_mean - (atr * atr_multiplier)

        return upper_kc, lower_kc

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if not data:
            self.stdout.write("No data fetched from the database.")
            return

        self.stdout.write(f"Fetched {len(data)} data points.")

        # Extract fields
        symbols = [item["symbol"] for item in data]
        highs = [float(item["high"]) for item in data]
        lows = [float(item["low"]) for item in data]
        closes = [float(item["ltp"]) for item in data]  # Assuming LTP is used as the close price
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if len(symbols) != len(highs) or len(symbols) != len(lows) or len(symbols) != len(closes) or len(symbols) != len(timestamps):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Calculate Squeeze Pro for each symbol
            for i in range(20, len(closes)):  # Ensure we have enough data for the first period (20)
                symbol = symbols[i]
                timestamp = timestamps[i]
                high_prices_window = highs[i-20:i]  # Last 20 high prices
                low_prices_window = lows[i-20:i]  # Last 20 low prices
                close_prices_window = closes[i-20:i]  # Last 20 closing prices

                # Calculate Bollinger Bands and Keltner Channels
                upper_bb, lower_bb = self.calculate_bollinger_bands(close_prices_window)
                upper_kc, lower_kc = self.calculate_keltner_channels(high_prices_window, low_prices_window, close_prices_window)

                # Squeeze condition: BB inside KC
                squeeze_condition = upper_bb.iloc[-1] < upper_kc.iloc[-1] and lower_bb.iloc[-1] > lower_kc.iloc[-1]

                # Signal based on the squeeze breakout
                if squeeze_condition:
                    signal = "Squeeze"
                else:
                    # Check for breakout (BB outside KC)
                    if upper_bb.iloc[-1] > upper_kc.iloc[-1]:
                        signal = "Breakout Up"
                    elif lower_bb.iloc[-1] < lower_kc.iloc[-1]:
                        signal = "Breakout Down"
                    else:
                        signal = "Neutral"

                # Save to database
                SqueezeProModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "squeeze_pro": squeeze_condition,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - Squeeze Pro: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating Squeeze Pro: {str(e)}")
