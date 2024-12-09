import csv
from datetime import datetime
from scripts.models import AllScriptsData

def load_csv_to_db(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Handle date conversion (MM/DD/YYYY format in CSV)
                date = datetime.strptime(row['Date'], '%m/%d/%Y').date() if row.get('Date') else None
                time = row.get('time')  # Assuming there's no time in this CSV, skip it

                # Remove commas and convert to float
                ltp = float(row['LTP'].replace(',', '')) if row.get('LTP') else None
                percent_change = float(row['% Change'].replace(',', '')) if row.get('% Change') else None
                high = float(row['High'].replace(',', '')) if row.get('High') else None
                low = float(row['Low'].replace(',', '')) if row.get('Low') else None
                open_price = float(row['Open'].replace(',', '')) if row.get('Open') else None
                volume = float(row['Qty.'].replace(',', '')) if row.get('Qty.') else None
                turnover = float(row['Turnover'].replace(',', '')) if row.get('Turnover') else None

                # Create and save the model instance
                AllScriptsData.objects.create(
                    symbol=row.get('Symbol'),
                    ltp=ltp,
                    percentChange=percent_change,
                    high=high,
                    low=low,
                    open=open_price,
                    volume=volume,
                    turnover=turnover,
                    date=date,
                    time=None  # No time provided in your data
                )
            except Exception as e:
                print(f"Error inserting row: {row}. Error: {e}")

load_csv_to_db('/home/volcussoft-djangosite/htdocs/djangosite.volcussoft.com/laganisutra/ohlcv_data/2021_scraped_data_with_dates.csv')
