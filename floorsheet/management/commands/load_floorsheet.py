import csv
from django.core.management.base import BaseCommand
from floorsheet.models import FloorSheetData

class Command(BaseCommand):
    help = "Imports data from floorsheet_data.csv into the FloorSheetData model."

    def handle(self, *args, **kwargs):
        file_path = '/Users/faizansari/Downloads/analysis/scrapper/data/floorsheet_data.csv' # Ensure this path is correct

        try:
            with open(file_path, mode='r') as file:
                reader = csv.DictReader(file)
                data_list = []

                for row in reader:
                    data = FloorSheetData(
                        transaction_no=int(row['Transact. No.']),
                        symbol=row['Symbol'],
                        buyer=row['Buyer'],
                        seller=row['Seller'],
                        quantity=row['Quantity'],
                        rate=row['Rate'],
                        amount=row['Amount'],
                        date='2024-11-29'
                    )
                    data_list.append(data)

                # Bulk insert for better performance
                FloorSheetData.objects.bulk_create(data_list)
                self.stdout.write(self.style.SUCCESS('Data imported successfully!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {file_path} not found."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {str(e)}"))
