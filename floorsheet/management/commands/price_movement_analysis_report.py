from django.core.management.base import BaseCommand
from django.db.models import Max as MaxAggregate
from floorsheet.models import FloorSheetData, PriceMovementAnalysisReport
from decimal import Decimal

class Command(BaseCommand):
    help = "Calculate Price Movement Analysis Report based on the latest FloorSheetData"

    def handle(self, *args, **kwargs):
        # Fetch the latest date
        latest_date = FloorSheetData.objects.aggregate(latest_date=MaxAggregate('date'))['latest_date']
        
        # Fetch the latest data for the latest date
        latest_data = FloorSheetData.objects.filter(date=latest_date)

        # Group by stock symbol
        stock_symbols = latest_data.values('symbol').distinct()

        for symbol in stock_symbols:
            symbol_data = latest_data.filter(symbol=symbol['symbol'])
            
            if symbol_data.exists():
                # Get the first and last rate values
                first_rate_str = symbol_data.first().rate
                last_rate_str = symbol_data.last().rate

                # Remove commas from the rate values
                first_rate = Decimal(first_rate_str.replace(',', ''))
                last_rate = Decimal(last_rate_str.replace(',', ''))

                # Calculate the percent change
                percent_change = ((last_rate - first_rate) / first_rate) * 100

                # Determine the trend
                if percent_change > 0:
                    trend = "Upward"
                elif percent_change < 0:
                    trend = "Downward"
                else:
                    trend = "Stable"

                # Store the result in the PriceMovementAnalysisReport model
                report = PriceMovementAnalysisReport(
                    symbol=symbol['symbol'],
                    first_rate=first_rate,
                    last_rate=last_rate,
                    percent_change=round(percent_change, 2),
                    trend=trend,
                    date=latest_date
                )
                report.save()

                self.stdout.write(self.style.SUCCESS(f"Report for {symbol['symbol']} saved successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"No data found for {symbol['symbol']} on {latest_date}"))
