from django.core.management.base import BaseCommand
from django.db.models import Sum
from floorsheet.models import FloorSheetData, LiquidityConcentrationReport
from decimal import Decimal
from django.db.models import Max

class Command(BaseCommand):
    help = "Calculate Liquidity Concentration Ratio (LCR) Report"

    def handle(self, *args, **kwargs):
        # Fetch the latest date
        latest_date = FloorSheetData.objects.aggregate(latest_date=Max('date'))['latest_date']
        
        # Fetch the latest data for the latest date
        latest_data = FloorSheetData.objects.filter(date=latest_date)

        # Clean up the quantity data by removing commas (if any)
        for entry in latest_data:
            if entry.quantity:
                entry.quantity = entry.quantity.replace(',', '')
                entry.save()

        # Calculate the total quantity traded for all symbols on the latest date
        total_quantity_all_symbols = latest_data.aggregate(total_quantity=Sum('quantity'))['total_quantity']

        # Group by stock symbol
        stock_symbols = latest_data.values('symbol').distinct()

        for symbol in stock_symbols:
            symbol_data = latest_data.filter(symbol=symbol['symbol'])

            if symbol_data.exists():
                # Calculate total quantity traded for the stock symbol
                total_quantity_traded = symbol_data.aggregate(total_quantity=Sum('quantity'))['total_quantity']
                
                if total_quantity_all_symbols > 0:
                    # Calculate the Liquidity Concentration Ratio (LCR %)
                    lcr_percentage = (Decimal(total_quantity_traded) / Decimal(total_quantity_all_symbols)) * 100
                else:
                    lcr_percentage = Decimal(0)  # To avoid division by zero

                # Determine the Liquidity Concentration and Interpretation based on LCR %
                if 0 <= lcr_percentage <= 20:
                    liquidity_concentration = "Very Low Concentration"
                    interpretation = "Liquidity is very evenly distributed across all assets."
                elif 21 <= lcr_percentage <= 40:
                    liquidity_concentration = "Low Concentration"
                    interpretation = "Liquidity is relatively well-distributed, but with slight concentration."
                elif 41 <= lcr_percentage <= 60:
                    liquidity_concentration = "Moderate Concentration"
                    interpretation = "Some concentration in a few assets, but still fairly balanced."
                elif 61 <= lcr_percentage <= 80:
                    liquidity_concentration = "High Concentration"
                    interpretation = "Liquidity is concentrated in fewer assets, indicating reduced diversity."
                elif 81 <= lcr_percentage <= 100:
                    liquidity_concentration = "Very High Concentration"
                    interpretation = "Liquidity is highly concentrated in a small number of assets."

                # Store the result in the LiquidityConcentrationReport model
                report = LiquidityConcentrationReport(
                    symbol=symbol['symbol'],
                    total_quantity_traded=total_quantity_traded,
                    lcr_percentage=round(lcr_percentage, 2),
                    liquidity_concentration=liquidity_concentration,
                    interpretation=interpretation,
                    date=latest_date
                )
                report.save()

                self.stdout.write(self.style.SUCCESS(f"Report for {symbol['symbol']} saved successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"No data found for {symbol['symbol']} on {latest_date}"))
