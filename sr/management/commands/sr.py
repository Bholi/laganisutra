from django.core.management.base import BaseCommand
from sr.models import SupportResistance
from livedata.models import LiveFeedData
import pandas as pd

class Command(BaseCommand):
    help = "Calculate support and resistance lines and save them to the database"

    def handle(self, *args, **kwargs):
        data = LiveFeedData.objects.all().values(
            'datetime', 'symbol', 'high', 'low', 'previous_closing'
        )
        if not data.exists():
            self.stdout.write(self.style.ERROR("No data available in LiveFeedData."))
            return

        df = pd.DataFrame(data)
        df['high'] = pd.to_numeric(df['high'], errors='coerce')
        df['low'] = pd.to_numeric(df['low'], errors='coerce')
        df['close'] = pd.to_numeric(df['previous_closing'], errors='coerce')

        df['pivot'] = (df['high'] + df['low'] + df['close']) / 3
        df['resistance_1'] = (2 * df['pivot']) - df['low']
        df['support_1'] = (2 * df['pivot']) - df['high']
        df['resistance_2'] = df['pivot'] + (df['high'] - df['low'])
        df['support_2'] = df['pivot'] - (df['high'] - df['low'])

        # Save the calculated values to the database
        for _, row in df.iterrows():
            if pd.notnull(row['datetime']) and pd.notnull(row['symbol']):
                SupportResistance.objects.update_or_create(
                    datetime=row['datetime'],
                    symbol=row['symbol'],
                    defaults={
                        "pivot": row['pivot'],
                        "resistance_1": row['resistance_1'],
                        "support_1": row['support_1'],
                        "resistance_2": row['resistance_2'],
                        "support_2": row['support_2'],
                    }
                )

        self.stdout.write(self.style.SUCCESS("Support and Resistance values saved to the database"))
