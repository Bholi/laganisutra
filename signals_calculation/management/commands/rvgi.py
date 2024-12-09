import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import RVGIModel  # Assuming RVGIModel exists for storing RVGI data
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate RVGI, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch data from the database ordered by datetime.
        """
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol', 'high', 'low','ltp','open','datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []
        

    def calculate_rvgi(self, high_prices, low_prices, close_prices, open_prices):
        """
        Calculate the Relative Vigor Index (RVGI).
        """
        rvgi_values = []

        for i in range(len(high_prices)):
            close = close_prices[i]
            open_ = open_prices[i]
            high = high_prices[i]
            low = low_prices[i]

            if high - low != 0:
                rvgi = (close - open_) / (high - low)
            else:
                rvgi = 0  # Avoid division by zero

            rvgi_values.append(rvgi)

        # Convert to pandas series for smoothing (EMA)
        rvgi_series = pd.Series(rvgi_values)

        # Apply an EMA to smooth the RVGI values
        smoothed_rvgi = rvgi_series.ewm(span=14, adjust=False).mean()

        return smoothed_rvgi

    def calculate_signal(self, rvgi_value):
        """
        Generate a signal based on the RVGI value.
        """
        if rvgi_value > 0.5:
            return "Strong"
        elif rvgi_value < -0.5:
            return "Weak"
        else:
            return "Neutral"

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
        closes = [float(item["ltp"]) for item in data]
        opens = [float(item["open"].replace(',', '')) for item in data] # Assuming open price is the same as LTP for simplicity
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if not (len(symbols) == len(highs) == len(lows) == len(closes) == len(opens) == len(timestamps)):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Calculate RVGI values
            rvgi_values = self.calculate_rvgi(highs, lows, closes, opens)

            # Skip NaN values (initial values for RVGI calculation)
            for i in range(14, len(rvgi_values)):
                rvgi_value = rvgi_values.iloc[i]

                if pd.isna(rvgi_value):  # Skip if RVGI is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - RVGI is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal based on RVGI value
                signal = self.calculate_signal(rvgi_value)

                # Save to database
                RVGIModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "rvgi": rvgi_value,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - RVGI: {rvgi_value:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating RVGI: {str(e)}")
