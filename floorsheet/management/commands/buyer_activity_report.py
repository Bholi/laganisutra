from django.db.models import Sum, Min, Max, Avg, F, Value, FloatField, Case, When
from django.db.models.functions import Cast, Replace, Coalesce
from django.core.management.base import BaseCommand
from floorsheet.models import FloorSheetData, BuyerActivityReport


class Command(BaseCommand):
    help = 'Aggregate FloorSheetData and store results in Buyer Activity Report'

    def handle(self, *args, **kwargs):
        # Fetch the latest date using Max
        latest_date = FloorSheetData.objects.aggregate(latest_date=Max('date'))['latest_date']

        if latest_date:
            print(f"Calculating activity for the latest date: {latest_date}")

            # Filter and clean the data for the latest date
            cleaned_data = FloorSheetData.objects.filter(date=latest_date).annotate(
                clean_quantity=Coalesce(
                    Cast(
                        Case(
                            When(quantity__contains=',', then=Replace(F('quantity'), Value(','), Value(''))),
                            default=F('quantity'),
                            output_field=FloatField()
                        ),
                        FloatField()
                    ),
                    0.0
                ),
                clean_rate=Coalesce(
                    Cast(
                        Case(
                            When(rate__contains=',', then=Replace(F('rate'), Value(','), Value(''))),
                            default=F('rate'),
                            output_field=FloatField()
                        ),
                        FloatField()
                    ),
                    0.0
                ),
                clean_amount=Coalesce(
                    Cast(
                        Case(
                            When(amount__contains=',', then=Replace(F('amount'), Value(','), Value(''))),
                            default=F('amount'),
                            output_field=FloatField()
                        ),
                        FloatField()
                    ),
                    0.0
                )
            )

            # Debugging: Print the cleaned data to check if values are being converted correctly
            for data in cleaned_data:
                print(f"Cleaned data: Quantity={data.clean_quantity}, Rate={data.clean_rate}, Amount={data.clean_amount}")

            # Aggregate data: Calculate total quantity, total amount, min price, max price, and avg price
            buyer_data = cleaned_data.values('buyer', 'symbol').annotate(
                total_quantity_bought=Sum('clean_quantity'),
                total_amount_spent=Sum('clean_amount'),
                min_price=Min('clean_rate'),
                max_price=Max('clean_rate'),
                avg_price=Avg('clean_rate')  # This could still be null if clean_rate is null after cleaning
            )

            # Debugging: Print aggregated data
            for data in buyer_data:
                print(f"Aggregated data: {data}")

            # Store the calculated data in the BuyerActivityReport model
            for data in buyer_data:
                BuyerActivityReport.objects.create(
                    buyer_id=data['buyer'],
                    symbol=data['symbol'],
                    total_quantity_bought=data['total_quantity_bought'],
                    total_amount_spent=data['total_amount_spent'],
                    min_price=data['min_price'],
                    max_price=data['max_price'],
                    avg_price=data['avg_price'],
                    date=latest_date
                )

            print("Buyer activity report has been calculated and stored.")
        else:
            print("No data available in FloorSheetData.")
