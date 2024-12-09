# detect_ramping.py

import pandas as pd
from django.core.management.base import BaseCommand
from manupulation.models import RampingData

class Command(BaseCommand):
    help = 'Detect ramping activities from floorsheet data'

    def handle(self, *args, **kwargs):
        # Load the floorsheet data
        file_path = "/Users/faizansari/Downloads/analysis/scrapper/data/floorsheet_data.csv"
        df = pd.read_csv(file_path)

        # Convert 'Rate' and 'Quantity' to numeric, cleaning any commas if present
        df['Rate'] = pd.to_numeric(df['Rate'].str.replace(',', ''), errors='coerce')
        df['Quantity'] = pd.to_numeric(df['Quantity'].str.replace(',', ''), errors='coerce')

        # Initialize a column for Ramping Detection
        df['RampingFlag'] = False

        # Define thresholds for ramping detection
        price_increase_threshold = 0.05  # 5% increase in price
        volume_threshold = 1000  # Example threshold for volume

        # Loop through the DataFrame to detect ramping
        for i in range(1, len(df)):
            # Calculate the price change percentage
            price_change = (df['Rate'].iloc[i] - df['Rate'].iloc[i - 1]) / df['Rate'].iloc[i - 1]

            # Check if the price change exceeds the threshold and volume is high
            if price_change >= price_increase_threshold and df['Quantity'].iloc[i] > volume_threshold:
                df.at[i, 'RampingFlag'] = True

        # Prepare the output DataFrame
        output_df = df[['Transact. No.', 'Symbol', 'Buyer', 'Seller', 'Rate', 'Quantity', 'RampingFlag']]
        output_df.columns = ['transaction_no', 'symbol', 'buyer', 'seller', 'price', 'volume', 'ramping_flag']

        # Save the output to the database
        for _, row in output_df.iterrows():
            RampingData.objects.update_or_create(
                transaction_no=row['transaction_no'],
                symbol=row['symbol'],
                buyer=row['buyer'],
                seller=row['seller'],
                price=row['price'],
                volume=row['volume'],
                ramping_flag=row['ramping_flag']
            )

        self.stdout.write(self.style.SUCCESS('Ramping detection completed successfully.'))
