import pandas as pd
from django.core.management.base import BaseCommand
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from momentum.models import SlopeModel  # Assuming SlopeModel exists for storing slope data
from django.db.models import Max

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Slope, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch data from the database ordered by datetime.
        """
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol','ltp', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []
        

    def calculate_slope(self, close_prices, period=14):
        """
        Calculate the slope using linear regression on closing prices.
        """
        x = list(range(period))  # Create time periods [0, 1, 2, ..., period-1]
        y = close_prices[-period:]  # Get the last 'period' closing prices

        # Calculate the sums required for the linear regression formula
        n = period
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(x_i * y_i for x_i, y_i in zip(x, y))
        sum_x_squared = sum(x_i ** 2 for x_i in x)

        # Apply the linear regression formula for slope
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
        return slope

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
            # Calculate Slope
            for i in range(14, len(closes)):  # Ensure we have enough data for the first period (14)
                symbol = symbols[i]
                timestamp = timestamps[i]
                close_prices_window = closes[i-14:i]  # Last 14 closing prices

                # Calculate the slope for the window
                slope_value = self.calculate_slope(close_prices_window)

                # Determine signal based on Slope
                if slope_value > 0:
                    signal = "Uptrend"
                elif slope_value < 0:
                    signal = "Downtrend"
                else:
                    signal = "Neutral"

                # Save to database
                SlopeModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "slope": slope_value,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - Slope: {slope_value:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating Slope: {str(e)}")
