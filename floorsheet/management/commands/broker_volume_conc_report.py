from django.core.management.base import BaseCommand
from floorsheet.models import FloorSheetData, BrokerVolumeConcentrationReport
from django.db.models import Count, Sum
from django.db.models import Max

class Command(BaseCommand):
    help = "Generate Broker Volume Concentration Report"

    def handle(self, *args, **kwargs):
        # Fetch the latest date
        latest_date = FloorSheetData.objects.aggregate(latest_date=Max('date'))['latest_date']
        
        # Fetch the data for the latest date
        latest_data = FloorSheetData.objects.filter(date=latest_date)
        
        # Group by stock symbol and perform aggregation
        stock_symbols = latest_data.values('symbol').distinct()

        for symbol in stock_symbols:
            symbol_data = latest_data.filter(symbol=symbol['symbol'])
            
            if symbol_data.exists():
                # Calculate the number of unique buying brokers
                buying_brokers = symbol_data.filter(buyer__isnull=False).values('buyer').distinct().count()
                
                # Calculate the number of unique selling brokers
                selling_brokers = symbol_data.filter(seller__isnull=False).values('seller').distinct().count()
                
                # Calculate total share quantity
                total_quantity = symbol_data.aggregate(Sum('quantity'))['quantity__sum']
                
                # Clean quantity data by removing commas (if any)
                total_quantity = str(total_quantity).replace(',', '') if total_quantity else '0'
                total_quantity = float(total_quantity)
                
                # Calculate the total number of transactions
                num_transactions = symbol_data.count()

                # Store the result in the BrokerVolumeConcentrationReport model
                report = BrokerVolumeConcentrationReport(
                    symbol=symbol['symbol'],
                    buying_brokers=buying_brokers,
                    selling_brokers=selling_brokers,
                    share_quantity=round(total_quantity, 2),
                    num_transactions=num_transactions,
                    date = latest_date
                )
                report.save()

                self.stdout.write(self.style.SUCCESS(f"Broker Volume Concentration Report for {symbol['symbol']} saved successfully!"))
            else:
                self.stdout.write(self.style.WARNING(f"No data found for {symbol['symbol']} on {latest_date}"))
