from django.core.management.base import BaseCommand
from floorsheet.models import FloorSheetData, PriceElasticityDemandReport
from decimal import Decimal
from django.db.models import Max
class Command(BaseCommand):
    help = "Generate Price Elasticity of Demand Report"

    def handle(self, *args, **kwargs):
        # Fetch the latest date
        latest_date = FloorSheetData.objects.aggregate(latest_date=Max('date'))['latest_date']
        
        # Fetch the latest data for the latest date
        latest_data = FloorSheetData.objects.filter(date=latest_date)
        
        # Group by stock symbol
        stock_symbols = latest_data.values('symbol').distinct()

        for symbol in stock_symbols:
            symbol_data = latest_data.filter(symbol=symbol['symbol'])
            
            if symbol_data.exists():
                # Calculate first and last rates and quantities (assuming quantity is in the data)
                first_rate = symbol_data.first().rate
                last_rate = symbol_data.last().rate
                first_quantity = symbol_data.first().quantity  # Assuming quantity is the field for demand
                last_quantity = symbol_data.last().quantity
                
                # Clean quantity and rate data by removing commas (if any)
                first_rate = first_rate.replace(',', '') if first_rate else '0'
                last_rate = last_rate.replace(',', '') if last_rate else '0'
                first_quantity = first_quantity.replace(',', '') if first_quantity else '0'
                last_quantity = last_quantity.replace(',', '') if last_quantity else '0'
                
                # Convert to Decimal for calculation
                first_rate = float(first_rate)
                last_rate = float(last_rate)
                first_quantity = float(first_quantity)
                last_quantity = float(last_quantity)

                # Calculate Price Change (%) and Quantity Change (%)
                price_change_percentage = ((last_rate - first_rate) / first_rate) * 100 if first_rate != 0 else 0
                quantity_change_percentage = ((last_quantity - first_quantity) / first_quantity) * 100 if first_quantity != 0 else 0

                # Calculate Price Elasticity of Demand (PED)
                if quantity_change_percentage != 0:
                    ped = abs(price_change_percentage) / abs(quantity_change_percentage)
                else:
                    ped = Decimal(0)

                # Determine Market Condition and Interpretation based on PED
                if ped > 1:
                    market_condition = "Elastic Demand"
                    interpretation = "A relatively small change in price causes a large change in the quantity demanded."
                elif ped < 1:
                    market_condition = "Inelastic Demand"
                    interpretation = "A relatively large change in price causes a smaller change in quantity demanded."
                elif ped == 1:
                    market_condition = "Unitary Elastic"
                    interpretation = "The change in price results in a proportional change in quantity demanded."

                # Store the result in the PriceElasticityDemandReport model
                report = PriceElasticityDemandReport(
                    symbol=symbol['symbol'],
                    price_change_percentage=round(price_change_percentage, 2),
                    quantity_change_percentage=round(quantity_change_percentage, 2),
                    ped=round(ped, 2),
                    market_condition=market_condition,
                    interpretation=interpretation,
                    date = latest_date,
                )
                report.save()

                self.stdout.write(self.style.SUCCESS(f"Report for {symbol['symbol']} saved successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"No data found for {symbol['symbol']} on {latest_date}"))
