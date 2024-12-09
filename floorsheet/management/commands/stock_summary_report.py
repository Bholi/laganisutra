from django.core.management.base import BaseCommand
from django.db.models import Max, Sum, Count, F, FloatField, Value, Case, When
from django.db.models.functions import Cast, Replace
from floorsheet.models import FloorSheetData, StockSummaryReport

class Command(BaseCommand):
    help = 'Aggregate FloorSheetData and store results in AggregatedFloorSheetData'

    def handle(self, *args, **kwargs):
        # Fetch the latest date using Max
        latest_date = FloorSheetData.objects.aggregate(latest_date=Max('date'))['latest_date']

        if latest_date:
            self.stdout.write(f"Latest date found: {latest_date}")

            # Filter data for the latest date
            latest_data = FloorSheetData.objects.filter(date=latest_date)

            # Preprocess the quantity and rate fields
            latest_data = latest_data.annotate(
                clean_quantity=Cast(
                    Case(
                        When(quantity__contains=',', then=Replace(F('quantity'), Value(','), Value(''))),
                        default=F('quantity'),
                        output_field=FloatField()
                    ),
                    FloatField()
                ),
                clean_rate=Cast(
                    Case(
                        When(rate__contains=',', then=Replace(F('rate'), Value(','), Value(''))),
                        default=F('rate'),
                        output_field=FloatField()
                    ),
                    FloatField()
                )
            )

            # Aggregate data: Calculate total quantity traded, number of transactions, total value, and average rate for each symbol
            aggregated_data = latest_data.values('symbol').annotate(
                total_quantity_traded=Sum('clean_quantity'),
                no_of_transactions=Count('transaction_no'),
                total_value=Sum(F('clean_quantity') * F('clean_rate')),  # Calculate total value
                average_rate=Sum(F('clean_quantity') * F('clean_rate')) / Sum('clean_quantity')  # Calculate average rate
            )

            # Store aggregated data in the new model
            for data in aggregated_data:
                StockSummaryReport.objects.create(
                    symbol=data['symbol'],
                    total_quantity_traded=data['total_quantity_traded'],
                    no_of_transactions=data['no_of_transactions'],
                    total_value=data['total_value'],
                    average_rate=data['average_rate'],
                    date=latest_date
                )

            self.stdout.write(self.style.SUCCESS("Aggregation and storage completed successfully."))
        else:
            self.stdout.write(self.style.WARNING("No data available in FloorSheetData."))
