import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import PSLModel  # Assuming PSLModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from django.db.models import Max


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate PSL, and store it in the database'

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
        

    def calculate_psl(self, close_prices, period=14):
        """
        Calculate the Psychological Line (PSL) for a given period.
        """
        close_prices = pd.Series(close_prices)

        # Compare each close with the previous close
        up_periods = close_prices.diff().apply(lambda x: 1 if x > 0 else 0)

        # Calculate rolling sum of up periods and percentage
        psl = up_periods.rolling(window=period).sum() / period * 100
        return psl

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if not data:
            self.stdout.write("No data fetched from the database.")
            return

        self.stdout.write(f"Fetched {len(data)} data points.")

        # Extract fields
        symbols = [item["symbol"] for item in data]
        closes = [float(item["ltp"]) for item in data]
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if not (len(symbols) == len(closes) == len(timestamps)):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Calculate PSL values
            psl_values = self.calculate_psl(closes)

            # Skip NaN values (initial values for rolling calculation)
            for i in range(14, len(psl_values)):  # Skip initial period
                psl = psl_values.iloc[i]

                if pd.isna(psl):
                    self.stdout.write(f"Skipping {symbols[i]} - PSL is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Buy" if psl > 50 else "Sell" if psl < 50 else "Neutral"

                # Save to database
                PSLModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "psl_value": psl,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - PSL: {psl:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating PSL: {str(e)}")
