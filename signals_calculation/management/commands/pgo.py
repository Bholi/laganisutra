import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import PGOModel  # Assuming PGOModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate PGO, and store it in the database'

    def fetch_data_from_db(self):
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime__lte=latest_datetime).values(
                'symbol', 'ltp', 'high', 'low', 'datetime'
            )
            return list(data)
        return []

    def calculate_pgo(self, close_prices, high_prices, low_prices, period=14):
        close_prices = pd.Series(close_prices)
        high_prices = pd.Series(high_prices)
        low_prices = pd.Series(low_prices)

        # Check data sufficiency
        if len(close_prices) < period:
            raise ValueError("Not enough data points to calculate PGO")

        # Moving Average
        ma_close = close_prices.rolling(window=period).mean()

        # True Range
        tr = pd.Series([
            max(high - low, abs(high - prev_close), abs(low - prev_close))
            for high, low, prev_close in zip(high_prices[1:], low_prices[1:], close_prices[:-1])
        ])
        tr = pd.concat([pd.Series([None]), tr])  # Align with original series

        # Average True Range
        atr = tr.rolling(window=period).mean()

        # Pretty Good Oscillator
        pgo = (close_prices - ma_close) / atr

        return pgo

    def handle(self, *args, **kwargs):
        data = self.fetch_data_from_db()

        # Validate data
        if not data:
            self.stdout.write("No data fetched from the database.")
            return

        self.stdout.write(f"Fetched {len(data)} data points.")

        symbols = [item["symbol"] for item in data]
        closes = [float(item["ltp"]) for item in data]
        highs = [float(item["high"]) for item in data]
        lows = [float(item["low"]) for item in data]
        timestamps = [item["datetime"] for item in data]

        # Ensure all lists are of the same length
        if not (len(symbols) == len(closes) == len(highs) == len(lows) == len(timestamps)):
            self.stdout.write("Data length mismatch between fields.")
            return

        try:
            pgo_values = self.calculate_pgo(closes, highs, lows)

            # Skip initial NaN values
            for i in range(14, len(pgo_values)):  # Skip values for the rolling window period
                pgo = pgo_values.iloc[i]

                if pd.isna(pgo):
                    self.stdout.write(f"Skipping {symbols[i]} - PGO is NaN")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Signal determination
                signal = "Buy" if pgo > 0 else "Sell" if pgo < 0 else "Neutral"

                # Save to database
                PGOModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "pgo_value": pgo,
                        "signal": signal
                    }
                )
                self.stdout.write(f"Saved {symbol} - PGO: {pgo:.4f}, Signal: {signal}")

        except ValueError as e:
            self.stdout.write(str(e))
