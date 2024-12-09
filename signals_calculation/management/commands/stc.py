import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import STCModel  # Assuming STCModel exists for storing STC data
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate STC, and store it in the database'

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
        

    def calculate_macd(self, close_prices):
        """
        Calculate MACD (12, 26) and Signal Line (9) using Exponential Moving Average.
        """
        macd = pd.Series(close_prices).ewm(span=12, adjust=False).mean() - pd.Series(close_prices).ewm(span=26, adjust=False).mean()
        signal_line = macd.ewm(span=9, adjust=False).mean()
        return macd, signal_line

    def calculate_stochastic(self, macd_values, period=9):
        """
        Calculate the Stochastic Oscillator based on the MACD values.
        """
        lowest_macd = macd_values.rolling(window=period).min()
        highest_macd = macd_values.rolling(window=period).max()

        stochastic_oscillator = 100 * (macd_values - lowest_macd) / (highest_macd - lowest_macd)
        return stochastic_oscillator

    def calculate_stc(self, stochastic_oscillator):
        """
        Calculate the Schaff Trend Cycle (STC).
        """
        stc = stochastic_oscillator.ewm(span=3, adjust=False).mean()  # Apply EMA to smooth the Stochastic Oscillator
        return stc

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if not data:
            self.stdout.write("No data fetched from the database.")
            return

        self.stdout.write(f"Fetched {len(data)} data points.")

        # Extract fields
        symbols = [item["symbol"] for item in data]
        closes = [float(item["ltp"]) for item in data]  # Assuming LTP is used as the close price
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if len(symbols) != len(closes) or len(symbols) != len(timestamps):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Calculate MACD
            macd_values, signal_line = self.calculate_macd(closes)

            # Calculate Stochastic Oscillator
            stochastic_oscillator = self.calculate_stochastic(macd_values)

            # Calculate STC
            stc_values = self.calculate_stc(stochastic_oscillator)

            # Skip NaN values (initial values for STC calculation)
            for i in range(26, len(stc_values)):  # Skip the first 26 values due to MACD calculation window
                stc_value = stc_values.iloc[i]

                if pd.isna(stc_value):  # Skip if STC is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - STC is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal based on STC value
                if stc_value > 75:
                    signal = "Strong Buy"
                elif stc_value < 25:
                    signal = "Strong Sell"
                else:
                    signal = "Neutral"

                # Save to database
                STCModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "stc": stc_value,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - STC: {stc_value:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating STC: {str(e)}")
