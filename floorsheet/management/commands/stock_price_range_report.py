from django.core.management.base import BaseCommand
from floorsheet.models import FloorSheetData, StockPriceRangeReport
from decimal import Decimal
from django.db.models import Max,Min

class Command(BaseCommand):
    help = "Generate Stock Price Range Analysis Report"

    def handle(self, *args, **kwargs):
        # Fetch the latest date
        latest_date = FloorSheetData.objects.aggregate(latest_date=Max('date'))['latest_date']
        
        # Fetch the data for the latest date
        latest_data = FloorSheetData.objects.filter(date=latest_date)
        
        # Group by stock symbol
        stock_symbols = latest_data.values('symbol').distinct()

        for symbol in stock_symbols:
            symbol_data = latest_data.filter(symbol=symbol['symbol'])
            
            if symbol_data.exists():
                # Get the highest and lowest prices for the stock symbol
                highest_price = symbol_data.aggregate(Max('rate'))['rate__max']
                lowest_price = symbol_data.aggregate(Min('rate'))['rate__min']
                
                # Clean rate data by removing commas (if any)
                highest_price = highest_price.replace(',', '') if highest_price else '0'
                lowest_price = lowest_price.replace(',', '') if lowest_price else '0'
                
                # Convert to Decimal for calculation
                highest_price = float(highest_price)
                lowest_price = float(lowest_price)

                # Calculate Price Range (Rs)
                price_range = highest_price - lowest_price

                # Store the result in the StockPriceRangeReport model
                report = StockPriceRangeReport(
                    symbol=symbol['symbol'],
                    highest_price=round(highest_price, 2),
                    lowest_price=round(lowest_price, 2),
                    price_range=round(price_range, 2),
                    date = latest_date
                )
                report.save()

                self.stdout.write(self.style.SUCCESS(f"Stock Price Range Report for {symbol['symbol']} saved successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"No data found for {symbol['symbol']} on {latest_date}"))
