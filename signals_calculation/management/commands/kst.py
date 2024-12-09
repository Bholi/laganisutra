import pandas as pd
from django.core.management.base import BaseCommand
from django.db.models import Max
from momentum.models import KSTModel  # Assuming KstModel exists
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from datetime import datetime

class Command(BaseCommand):
    help = 'Fetch data from DB, calculate KST, and store it in the database'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']

        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime__lte=latest_datetime).values(
                'symbol', 'ltp', 'datetime'
            )
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_kst(self, close_prices, roc_periods=[10, 15, 20, 30], sma_periods=[10, 10, 10, 15]):
        """
        Calculate the KST (Know Sure Thing) values and Signal Line.

        Parameters:
        - close_prices: List of closing prices
        - roc_periods: List of periods for ROC calculations
        - sma_periods: List of smoothing periods for each ROC

        Returns:
        - kst_values: Series of KST values
        - signal_values: Series of Signal Line values
        """
        close_prices = pd.Series(close_prices)

        # Calculate Rate of Change (ROC) for specified periods
        roc_values = [close_prices.pct_change(period) * 100 for period in roc_periods]

        # Smooth each ROC using a Simple Moving Average (SMA)
        smoothed_roc = [roc.rolling(window=sma_period).mean() for roc, sma_period in zip(roc_values, sma_periods)]

        # Calculate the KST by summing the weighted smoothed ROC values
        weights = [1, 2, 3, 4]
        kst = sum(weight * smooth for weight, smooth in zip(weights, smoothed_roc))

        # Calculate the Signal Line (9-period SMA of KST)
        signal = kst.rolling(window=9).mean()

        return kst, signal

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            # Extract fields and ensure proper type conversion
            symbols = [item["symbol"] for item in data]
            closes = [float(item["ltp"]) for item in data]
            timestamps = [item["datetime"] for item in data]

            # Calculate KST values
            kst_values, signal_values = self.calculate_kst(closes)

            # Skip initial values with NaN due to rolling window
            for i in range(30, len(kst_values)):  # The longest period is 30
                kst = kst_values.iloc[i]
                signal = signal_values.iloc[i]

                if pd.isna(kst) or pd.isna(signal):  # Skip if any value is NaN
                    self.stdout.write(f"Skipping {symbols[i]} - KST or Signal has NaN values")
                    continue

                symbol = symbols[i]
                timestamp = timestamps[i]

                # Determine signal
                if kst > signal:
                    decision = "Buy"
                elif kst < signal:
                    decision = "Sell"
                else:
                    decision = "Neutral"

                # Save to database
                KSTModel.objects.update_or_create(
                    symbol=symbol,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "kst_value": kst,
                        "signal": decision
                    }
                )

                self.stdout.write(
                    f"Saved {symbol} - KST: {kst:.2f}, Signal: {signal:.2f}, Signal: {decision}"
                )
        else:
            self.stdout.write("No data to calculate KST.")
