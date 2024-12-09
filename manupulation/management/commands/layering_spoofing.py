# detect_layering_spoofing.py

import pandas as pd
from django.core.management.base import BaseCommand
from manupulation.models import LayeringSpoofingData

class Command(BaseCommand):
    help = 'Detect layering and spoofing from floorsheet data'

    def handle(self, *args, **kwargs):
        # Load the floorsheet data
        file_path = "/Users/faizansari/Downloads/analysis/scrapper/data/floorsheet_data.csv"
        df = pd.read_csv(file_path)

        # Convert 'Rate' and 'Quantity' to numeric, cleaning any commas if present
        df['Rate'] = pd.to_numeric(df['Rate'].str.replace(',', ''), errors='coerce')
        df['Quantity'] = pd.to_numeric(df['Quantity'].str.replace(',', ''), errors='coerce')

        # Initialize columns for layering and spoofing detection
        df['LayeringFlag'] = False
        df['SpoofingFlag'] = False

        # Thresholds for detection
        layering_threshold = 5  # Minimum number of orders at the same price to flag layering
        spoofing_order_count_threshold = 3  # Number of orders in a short period for spoofing

        # Detect Layering
        layering_counts = df.groupby(['Symbol', 'Rate']).size().reset_index(name='OrderCount')
        layering_flags = layering_counts[layering_counts['OrderCount'] >= layering_threshold]

        # Update the LayeringFlag in the original DataFrame
        df['LayeringFlag'] = df.apply(lambda row: row['Rate'] in layering_flags['Rate'].values and row['Symbol'] in layering_flags['Symbol'].values, axis=1)

        # Detect Spoofing
        df['OrderID'] = df.index  # Create a unique order ID for each entry
        df['OrderLag'] = df.groupby(['Buyer', 'Symbol'])['OrderID'].diff().fillna(0)

        # Flag orders with a high frequency that may indicate spoofing
        df['SpoofingFlag'] = df.groupby(['Buyer', 'Symbol'])['OrderLag'].transform(lambda x: x < 1).astype(bool)

        # Prepare the output DataFrame
        output_df = df[['Transact. No.', 'Symbol', 'Buyer', 'Seller', 'Rate', 'Quantity', 'LayeringFlag', 'SpoofingFlag']]
        output_df.columns = ['transaction_no', 'symbol', 'buyer', 'seller', 'price', 'volume', 'layering_flag', 'spoofing_flag']

        # Save the output to the database
        for _, row in output_df.iterrows():
            LayeringSpoofingData.objects.update_or_create(
                transaction_no=row['transaction_no'],
                symbol=row['symbol'],
                buyer=row['buyer'],
                seller=row['seller'],
                price=row['price'],
                volume=row['volume'],
                layering_flag=row['layering_flag'],
                spoofing_flag=row['spoofing_flag']
            )

        self.stdout.write(self.style.SUCCESS('Layering and spoofing detection completed successfully.'))
