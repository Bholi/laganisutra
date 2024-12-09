from django.core.management.base import BaseCommand
from django.db.models import Max
from livedata.models import LiveFeedData  # Assuming LiveFeedData is where data is stored
from pivot.models import CamrillaPivotPoint  # Assuming PivotPoint model is in momentum app
from datetime import datetime


class Command(BaseCommand):
    help = 'Fetch data from DB, calculate Camarilla levels, and store them in the PivotPoint model'

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

    def calculate_camarilla(self, high, low, ltp):
        """
        Calculate Camarilla pivot points: R1, R2, R3, R4, S1, S2, S3, S4.
        """
        diff = high - low
        factors = [1.1 / 12, 1.1 / 6, 1.1 / 4, 1.1 / 2]

        resistances = [ltp + diff * f for f in factors]
        supports = [ltp - diff * f for f in factors]

        return {
            "R1": resistances[0],
            "R2": resistances[1],
            "R3": resistances[2],
            "S1": supports[0],
            "S2": supports[1],
            "S3": supports[2],
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

                # Calculate Camarilla pivot points
                levels = self.calculate_camarilla(high, low, ltp)

                # Save the levels into the PivotPoint model
                CamrillaPivotPoint.objects.update_or_create(
                    script_name=script_name,
                    date=timestamp.date(),
                    time=timestamp.time(),
                    defaults={
                        "pivot_point": (high + low + ltp) / 3,  # This is the standard formula for PivotPoint
                        "r1": levels["R1"],
                        "r2": levels["R2"],
                        "r3": levels["R3"],
                        "s1": levels["S1"],
                        "s2": levels["S2"],
                        "s3": levels["S3"],
                    }
                )

                self.stdout.write(
                    f"Saved {script_name} - Pivot Point: {(high + low + ltp) / 3:.4f}, "
                    f"R1: {levels['R1']:.4f}, R2: {levels['R2']:.4f}, "
                    f"R3: {levels['R3']:.4f}, "
                    f"S1: {levels['S1']:.4f}, S2: {levels['S2']:.4f}, "
                    f"S3: {levels['S3']:.4f}"
                )
        else:
            self.stdout.write("No data to calculate Camarilla levels.")
