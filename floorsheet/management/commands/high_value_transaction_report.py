from django.db.models import F, Case, When, Value, FloatField
from django.db.models.functions import Cast, Replace
from django.core.management.base import BaseCommand
from floorsheet.models import FloorSheetData, HighValueTransactionReport
from django.db.models import Max

class Command(BaseCommand):
    help = 'Generate High-Value Transactions Report for the Latest Date'

    def handle(self, *args, **kwargs):
        # Fetch the latest date using Max
        latest_date = FloorSheetData.objects.aggregate(latest_date=Max('date'))['latest_date']

        if latest_date:
            print(f"Generating High-Value Transactions Report for the latest date: {latest_date}")

            # Fetch the data for the latest date and clean the data (remove commas)
            latest_data = FloorSheetData.objects.filter(date=latest_date).annotate(
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

            # Calculate the amount (quantity * rate)
            high_value_transactions = latest_data.annotate(
                calculated_amount=F('clean_quantity') * F('clean_rate')
            ).order_by('-calculated_amount')  # You can sort by the amount in descending order

            if high_value_transactions.exists():
                # Store the report data
                for transaction in high_value_transactions:
                    symbol = transaction.symbol
                    buyer = transaction.buyer
                    seller = transaction.seller
                    quantity = transaction.clean_quantity
                    rate = transaction.clean_rate
                    amount = transaction.calculated_amount

                    # Save the report data in the HighValueTransactionReport model
                    HighValueTransactionReport.objects.create(
                        symbol=symbol,
                        buyer=buyer,
                        seller=seller,
                        quantity=quantity,
                        rate=rate,
                        amount=amount,
                        date=latest_date
                    )

                print("High-Value Transactions Report has been generated successfully.")
            else:
                print("No transactions found for the latest date.")
        else:
            print("No data available for the latest date.")