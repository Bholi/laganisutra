from django.core.management.base import BaseCommand
from django.db.models import Max
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from pivot.models import FibonacciPivotPoint  # Assuming FibonacciPivotPoint model is in the momentum app



class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Fibonacci pivot points, and store them in the FibonacciPivotPoint model'

    def fetch_data_from_db(self):
        """
        Fetch the latest data from the database based on the datetime field.
        """
        latest_datetime = LiveFeedData.objects.aggregate(Max('datetime'))['datetime__max']
        if latest_datetime:
            data = LiveFeedData.objects.filter(datetime=latest_datetime).values('symbol', 'high', 'low', 'ltp', 'datetime')
            return list(data)
        else:
            self.stdout.write("No data found in the database.")
            return []

    def calculate_fibonacci(self, high, low, ltp):
        """
        Calculate Fibonacci pivot points: R1, R2, R3, S1, S2, S3.
        """
        diff = high - low
        pivot_point = (high + low + ltp) / 3

        # Fibonacci levels
        r1 = pivot_point + 0.382 * diff
        r2 = pivot_point + 0.618 * diff
        r3 = pivot_point + diff
        s1 = pivot_point - 0.382 * diff
        s2 = pivot_point - 0.618 * diff
        s3 = pivot_point - diff

        return {
            "pivot_point": pivot_point,
            "r1": r1,
            "r2": r2,
            "r3": r3,
            "s1": s1,
            "s2": s2,
            "s3": s3,
        }

    def handle(self, *args, **kwargs):
        # Fetch data from the database
        data = self.fetch_data_from_db()

        if data:
            for item in data:
                script_name = item['symbol']
                high = float(item['high'])
                low = float(item['low'])
                ltp = float(item['ltp'])
                timestamp = item['datetime']

                # Calculate Fibonacci pivot points
                levels = self.calculate_fibonacci(high, low, ltp)

                # Save the levels into the FibonacciPivotPoint model
                FibonacciPivotPoint.objects.update_or_create(
                    script_name=script_name,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "pivot_point": levels["pivot_point"],
                        "r1": levels["r1"],
                        "r2": levels["r2"],
                        "r3": levels["r3"],
                        "s1": levels["s1"],
                        "s2": levels["s2"],
                        "s3": levels["s3"],
                    }
                )

                self.stdout.write(
                    f"Saved {script_name} - Pivot Point: {levels['pivot_point']:.4f}, "
                    f"R1: {levels['r1']:.4f}, R2: {levels['r2']:.4f}, "
                    f"R3: {levels['r3']:.4f}, "
                    f"S1: {levels['s1']:.4f}, S2: {levels['s2']:.4f}, "
                    f"S3: {levels['s3']:.4f}"
                )
        else:
            self.stdout.write("No data to calculate Fibonacci pivot points.")
