from django.core.management.base import BaseCommand
from django.db.models import Sum, Min, Max, Avg, Count, FloatField, Value,F,Case,When
from django.db.models.functions import Cast, Replace
from floorsheet.models import FloorSheetData, TradeVolAnalysisReport

class Command(BaseCommand):
    help = "Generate Trade Volume Analysis Report"

    def handle(self, *args, **kwargs):
        # Fetch the latest date
        latest_date = FloorSheetData.objects.aggregate(latest_date=Max('date'))['latest_date']

        if latest_date:
            print(f"Generating Trade Volume Analysis Report for: {latest_date}")

            # Annotate clean_quantity by removing commas and converting to float
            cleaned_data = FloorSheetData.objects.filter(date=latest_date).annotate(
                clean_quantity=Cast(
                    Case(
                        When(quantity__contains=',', then=Replace(F('quantity'), Value(','), Value(''))),
                        default=F('quantity'),
                        output_field=FloatField()
                    ),
                    FloatField(),
                ),
                clean_amount=Cast(
                    Case(
                        When(amount__contains=',', then=Replace(F('amount'), Value(','), Value(''))),
                        default=F('amount'),
                        output_field=FloatField()
                    ),
                    FloatField(),
                )
            )

            # Aggregate data for each stock symbol
            trade_vol_analysis = cleaned_data.values('symbol').annotate(
                total_quantity_traded=Sum('clean_quantity'),
                no_of_transactions=Count('id'),
                min_trade_vol=Min('clean_amount'),
                max_trade_vol=Max('clean_amount'),
                avg_trade_volume=Avg('clean_amount')
            )

            # Save results to TradeVolAnalysisReport model
            for data in trade_vol_analysis:
                TradeVolAnalysisReport.objects.create(
                    symbol=data['symbol'],
                    total_quantity_traded=data['total_quantity_traded'],
                    no_of_transactions=data['no_of_transactions'],
                    min_trade_vol=data['min_trade_vol'],
                    max_trade_vol=data['max_trade_vol'],
                    avg_trade_volume=data['avg_trade_volume'],
                    date=latest_date
                )

            print("Trade Volume Analysis Report generated successfully.")
        else:
            print("No data available in FloorSheetData.")
