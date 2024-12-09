from django.db.models import Min, Max, Avg, StdDev, Case, When, F, Value, FloatField
from django.db.models.functions import Cast, Replace
from django.core.management.base import BaseCommand
from floorsheet.models import FloorSheetData, VolatilityAnalysisReport
from django.db.models import Max as MaxAggregate

class Command(BaseCommand):
    help = 'Generate Volatility Analysis Report for the Latest Date'

    def handle(self, *args, **kwargs):
        # Fetch the latest date using Max
        latest_date = FloorSheetData.objects.aggregate(latest_date=MaxAggregate('date'))['latest_date']

        if latest_date:
            print(f"Generating Volatility Analysis Report for the latest date: {latest_date}")

            # Fetch and clean data for the latest date (remove commas from rates)
            cleaned_data = FloorSheetData.objects.filter(date=latest_date).annotate(
                clean_rate=Cast(
                    Case(
                        When(rate__contains=',', then=Replace(F('rate'), Value(','), Value(''))),
                        default=F('rate'),
                        output_field=FloatField()
                    ),
                    FloatField()
                )
            )

            # Aggregate data to calculate min, max, avg, and stddev
            volatility_data = cleaned_data.values('symbol').annotate(
                min_rate=Min('clean_rate'),
                max_rate=Max('clean_rate'),
                avg_rate=Avg('clean_rate'),
                stddev_rate=StdDev('clean_rate')
            )

            # Store the results in VolatilityAnalysisReport
            for data in volatility_data:
                symbol = data['symbol']
                min_rate = data['min_rate']
                max_rate = data['max_rate']
                avg_rate = data['avg_rate']
                stddev_rate = data['stddev_rate']

                # Save the report data
                VolatilityAnalysisReport.objects.create(
                    symbol=symbol,
                    min_rate=min_rate,
                    max_rate=max_rate,
                    avg_rate=avg_rate,
                    stddev_rate=stddev_rate,
                    date=latest_date
                )

            print("Volatility Analysis Report has been generated successfully.")
        else:
            print("No data available for the latest date.")
