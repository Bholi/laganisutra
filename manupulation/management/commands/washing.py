# wash_trade_detection.py

import pandas as pd
from django.core.management.base import BaseCommand
from manupulation.models import WashTradeData

class Command(BaseCommand):
    help = 'Detect wash trades from floorsheet data'

    def handle(self, *args, **kwargs):
        # Load the floorsheet data
        file_path = "/Users/faizansari/Downloads/analysis/scrapper/data/floorsheet_data.csv"
        df = pd.read_csv(file_path)

        # Display initial information about the data
        print(df.head())
        print(df.info())
        print(f"Total unique symbols: {len(df['Symbol'].unique())}")
        print(df['Symbol'].unique())

        # Convert 'Rate' and 'Quantity' to numeric, cleaning commas if present
        df['Rate'] = pd.to_numeric(df['Rate'].str.replace(',', ''), errors='coerce')
        df['Quantity'] = pd.to_numeric(df['Quantity'].str.replace(',', ''), errors='coerce')

        # Initialize the WashTradeFlag to False for all rows
        df['WashTradeFlag'] = False

        # Process each symbol independently to detect wash trades
        for symbol in df['Symbol'].unique():
            symbol_df = df[df['Symbol'] == symbol].copy()
            symbol_df['WashTradeFlag'] = symbol_df['Buyer'] == symbol_df['Seller']
            df.loc[symbol_df.index, 'WashTradeFlag'] = symbol_df['WashTradeFlag']

        # Prepare DataFrame for saving to the database
        output_df = df[['Transact. No.', 'Symbol', 'Buyer', 'Seller', 'Rate', 'Quantity', 'WashTradeFlag']]
        output_df.columns = ['transaction_no', 'symbol', 'buyer', 'seller', 'price', 'volume', 'wash_trade_flag']

        # Save the data to the database
        for _, row in output_df.iterrows():
            WashTradeData.objects.update_or_create(
                transaction_no=row['transaction_no'],
                defaults={
                    'symbol': row['symbol'],
                    'buyer': row['buyer'],
                    'seller': row['seller'],
                    'price': row['price'],
                    'volume': row['volume'],
                    'wash_trade_flag': row['wash_trade_flag']
                }
            )

        self.stdout.write(self.style.SUCCESS('Wash trade detection completed successfully.'))
