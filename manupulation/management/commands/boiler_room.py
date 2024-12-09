# management/commands/process_floorsheet.py

import pandas as pd
from django.core.management.base import BaseCommand
from manupulation.models import BoilerRoom  # replace 'your_app' with the actual app name

class Command(BaseCommand):
    help = 'Process floorsheet data and store in the database'

    def handle(self, *args, **kwargs):
        # Load the floorsheet data
        file_path = "/Users/faizansari/Downloads/analysis/scrapper/data/floorsheet_data.csv"
        df = pd.read_csv(file_path)

        # Convert 'Rate' and 'Quantity' to numeric, cleaning any commas if present
        df['Rate'] = pd.to_numeric(df['Rate'].str.replace(',', ''), errors='coerce')
        df['Quantity'] = pd.to_numeric(df['Quantity'].str.replace(',', ''), errors='coerce')

        # Initialize columns for boiler room detection
        df['BoilerRoomFlag'] = False

        # Thresholds for detection
        high_trade_count_threshold = 10  # High volume threshold
        rapid_price_change_threshold = 0.1  # 10% change in price to flag rapid increase

        # Detect High Volume of Trades
        trade_counts = df['Symbol'].value_counts().reset_index(name='TradeCount')
        trade_counts.columns = ['Symbol', 'TradeCount']

        # Flag symbols with high trade counts
        high_volume_symbols = trade_counts[trade_counts['TradeCount'] >= high_trade_count_threshold]['Symbol'].values

        # Update the BoilerRoomFlag for high volume
        df['BoilerRoomFlag'] = df['Symbol'].isin(high_volume_symbols)

        # Detect Rapid Price Increases
        df['PriceChange'] = df.groupby('Symbol')['Rate'].pct_change()
        df['RapidPriceIncreaseFlag'] = df['PriceChange'].abs() >= rapid_price_change_threshold

        # Update the BoilerRoomFlag for rapid price increases
        df['BoilerRoomFlag'] |= df['RapidPriceIncreaseFlag']

        # Prepare data for saving to the database
        for _, row in df.iterrows():
            BoilerRoom.objects.create(
                transaction_no=row['Transact. No.'],
                symbol=row['Symbol'],
                buyer=row['Buyer'],
                seller=row['Seller'],
                price=row['Rate'],
                volume=row['Quantity'],
                boiler_room_flag=row['BoilerRoomFlag']  # Save the transaction number
            )

        self.stdout.write(self.style.SUCCESS('Floorsheet data processed and saved to the database.'))
