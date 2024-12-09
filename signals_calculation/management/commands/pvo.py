import pandas as pd
from django.core.management.base import BaseCommand
from momentum.models import PVOModel  # Assuming PVOModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from django.db.models import Max


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate PVO, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch data from the database ordered by datetime.
        """
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        
        # Fetch data with the latest datetime
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values(
                'symbol', 'volume', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []
        

    def calculate_pvo(self, volumes, short_period=12, long_period=26):
        """
        Calculate the Percentage Volume Oscillator (PVO) for given volume data.
        """
        volumes = pd.Series(volumes)

        # Calculate Short EMA and Long EMA
        short_ema = volumes.ewm(span=short_period, adjust=False).mean()
        long_ema = volumes.ewm(span=long_period, adjust=False).mean()

        # Calculate PVO
        pvo = ((short_ema - long_ema) / long_ema) * 100
        return pvo

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if not data:
            self.stdout.write("No data fetched from the database.")
            return

        self.stdout.write(f"Fetched {len(data)} data points.")

        # Extract fields
        symbols = [item["symbol"] for item in data]
        volumes = [float(item["volume"].replace(',', '')) for item in data]
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if not (len(symbols) == len(volumes) == len(timestamps)):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            # Calculate PVO values
            pvo_values = self.calculate_pvo(volumes)

            # Skip NaN values (initial values for EMA calculation)
            for i in range(max(12, 26), len(pvo_values)):  # Skip initial periods
                pvo = pvo_values.iloc[i]

                if pd.isna(pvo):
                    self.stdout.write(f"Skipping {symbols[i]} - PVO is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                signal = "Bullish" if pvo > 0 else "Bearish"

                # Save to database
                PVOModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "pvo_value": pvo,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - PVO: {pvo:.4f}, Signal: {signal}")

        except Exception as e:
            self.stdout.write(f"Error calculating PVO: {str(e)}")
