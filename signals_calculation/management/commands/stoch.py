import pandas as pd
from django.core.management.base import BaseCommand
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from momentum.models import StochasticOscillatorModel  # Assuming StochasticOscillatorModel exists for storing Stochastic data
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Stochastic Oscillator (Stoch), and store it in the database'

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
        

    def calculate_stochastic(self, high_prices, low_prices, close_prices, period=14):
        """
        Calculate Stochastic Oscillator (%K and %D).
        """
        lowest_low = pd.Series(low_prices).rolling(window=period).min()
        highest_high = pd.Series(high_prices).rolling(window=period).max()

        # Calculate %K
        stoch_k = 100 * (pd.Series(close_prices) - lowest_low) / (highest_high - lowest_low)

        # Calculate %D as the 3-period SMA of %K
        stoch_d = stoch_k.rolling(window=3).mean()

        return stoch_k, stoch_d

    def generate_signal(self, stoch_k, stoch_d):
        """
        Generate a buy or sell signal based on Stochastic Oscillator %K and %D.
        """
        # Generate signal based on %K and %D crossovers
        if stoch_k.iloc[-1] > stoch_d.iloc[-1]:
            signal = 'Buy'  # %K crosses above %D
        elif stoch_k.iloc[-1] < stoch_d.iloc[-1]:
            signal = 'Sell'  # %K crosses below %D
        else:
            signal = 'Neutral'  # No crossover

        # Additional overbought/oversold condition
        if stoch_k.iloc[-1] > 80:
            signal = 'Overbought'  # %K above 80
        elif stoch_k.iloc[-1] < 20:
            signal = 'Oversold'  # %K below 20

        return signal

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
            # Calculate Stochastic Oscillator for each symbol
            for i in range(14, len(closes)):  # Ensure we have enough data for the first period (14)
                symbol = symbols[i]
                timestamp = timestamps[i]
                high_prices_window = highs[i-14:i]  # Last 14 high prices
                low_prices_window = lows[i-14:i]  # Last 14 low prices
                close_prices_window = closes[i-14:i]  # Last 14 closing prices

                # Calculate Stochastic Oscillator
                stoch_k, stoch_d = self.calculate_stochastic(high_prices_window, low_prices_window, close_prices_window)

                # Generate Signal based on the %K and %D values
                signal = self.generate_signal(stoch_k, stoch_d)

                # Save to database
                StochasticOscillatorModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "k": stoch_k.iloc[-1],  # Latest %K value
                        "d": stoch_d.iloc[-1],  # Latest %D value
                        "signal": signal  # Save the generated signal (Buy/Sell/Neutral/Overbought/Oversold)
                    }
                )
                self.stdout.write(f"Saved {symbol} - Stochastic Oscillator: %K = {stoch_k.iloc[-1]}, %D = {stoch_d.iloc[-1]}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating Stochastic Oscillator: {str(e)}")
