from django.core.management.base import BaseCommand
from django.db.models import F
from floorsheet.models import FloorSheetData, PriceVolatilityVolumeReport
from decimal import Decimal
from django.db.models import Max

class Command(BaseCommand):
    help = "Generate Price Volatility vs. Volume Report"

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
                # Calculate first and last rates and volumes
                first_rate = symbol_data.first().rate
                last_rate = symbol_data.last().rate
                first_volume = symbol_data.first().amount  # Assuming amount is the volume field
                last_volume = symbol_data.last().amount
                
                # Clean amount and rate data by removing commas (if any)
                first_rate = first_rate.replace(',', '') if first_rate else '0'
                last_rate = last_rate.replace(',', '') if last_rate else '0'
                first_volume = first_volume.replace(',', '') if first_volume else '0'
                last_volume = last_volume.replace(',', '') if last_volume else '0'
                
                # Convert to Decimal for calculation
                first_rate = float(first_rate)
                last_rate = float(last_rate)
                first_volume = float(first_volume)
                last_volume = float(last_volume)

                # Calculate Price Change (%) and Volume Change (%)
                price_change_percentage = ((last_rate - first_rate) / first_rate) * 100 if first_rate != 0 else 0
                volume_change_percentage = ((last_volume - first_volume) / first_volume) * 100 if first_volume != 0 else 0

                # Calculate Volatility to Volume Ratio (VVR)
                if volume_change_percentage != 0:
                    vvr = abs(price_change_percentage) / abs(volume_change_percentage)
                else:
                    vvr = Decimal(0)

                # Determine Market Condition and Interpretation based on VVR
                if 0 <= vvr <= 0.5:
                    market_condition = "Low Volatility, High Volume"
                    interpretation = "Stable prices with strong market participation. Likely indicates accumulation."
                elif 0.6 <= vvr <= 1.0:
                    market_condition = "Moderate Balance"
                    interpretation = "Price movements moderately supported by volume. Normal market activity."
                elif 1.1 <= vvr <= 1.5:
                    market_condition = "Increasing Volatility"
                    interpretation = "Prices becoming more volatile relative to volume. Potential early signs of shifts."
                elif 1.6 <= vvr <= 2.0:
                    market_condition = "High Volatility"
                    interpretation = "Significant price changes with low volume. Possible speculative activity."
                elif vvr >= 2.1:
                    market_condition = "Extreme Volatility"
                    interpretation = "Prices moving unpredictably with little volume support. High risk and uncertainty."

                # Store the result in the PriceVolatilityVolumeReport model
                report = PriceVolatilityVolumeReport(
                    symbol=symbol['symbol'],
                    price_change_percentage=round(price_change_percentage, 2),
                    volume_change_percentage=round(volume_change_percentage, 2),
                    vvr=round(vvr, 2),
                    market_condition=market_condition,
                    interpretation=interpretation,
                    date = latest_date
                )
                report.save()

                self.stdout.write(self.style.SUCCESS(f"Report for {symbol['symbol']} saved successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"No data found for {symbol['symbol']} on {latest_date}"))
