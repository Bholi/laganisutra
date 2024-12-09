# detect_ponzi_scheme.py

import pandas as pd
from django.core.management.base import BaseCommand
from manupulation.models import PonziSchemeData

class Command(BaseCommand):
    help = 'Detect potential Ponzi schemes from floorsheet data'

    def handle(self, *args, **kwargs):
        # Load the floorsheet data
        file_path = "/Users/faizansari/Downloads/analysis/scrapper/data/floorsheet_data.csv"
        df = pd.read_csv(file_path)

        # Convert 'Rate' and 'Quantity' to numeric, cleaning any commas if present
        df['Rate'] = pd.to_numeric(df['Rate'].str.replace(',', ''), errors='coerce')
        df['Quantity'] = pd.to_numeric(df['Quantity'].str.replace(',', ''), errors='coerce')

        # Initialize a column for Ponzi Scheme Detection
        df['PonziFlag'] = False

        # Define thresholds for Ponzi detection
        high_return_threshold = 0.1  # Example threshold for high return (10%)
        volume_spike_factor = 2  # Example factor for volume spikes

        # Calculate returns and check for high returns
        df['PreviousRate'] = df['Rate'].shift(1)
        df['Return'] = (df['Rate'] - df['PreviousRate']) / df['PreviousRate']

        # Detect high return patterns
        df['PonziFlag'] |= df['Return'] >= high_return_threshold

        # Detect volume spikes
        df['VolumeSpike'] = df['Quantity'].shift(1) * volume_spike_factor
        df['PonziFlag'] |= df['Quantity'] > df['VolumeSpike']

        # Check for dependence on new investors
        total_invested = df['Quantity'].sum()
        total_returned = df['Rate'].sum()  # Assuming rate as return, adjust as necessary
        if total_returned / total_invested > 0.9:  # If 90% of investments are returned
            df['PonziFlag'] = True

        # Prepare the output DataFrame
        output_df = df[['Transact. No.', 'Symbol', 'Buyer', 'Seller', 'Rate', 'Quantity', 'PonziFlag']]
        output_df.columns = ['transaction_no', 'symbol', 'buyer', 'seller', 'price', 'volume', 'ponzi_flag']

        # Save the output to the database
        for _, row in output_df.iterrows():
            PonziSchemeData.objects.update_or_create(
                transaction_no=row['transaction_no'],
                symbol=row['symbol'],
                buyer=row['buyer'],
                seller=row['seller'],
                price=row['price'],
                volume=row['volume'],
                ponzi_flag=row['ponzi_flag']
            )

        self.stdout.write(self.style.SUCCESS('Ponzi scheme detection completed successfully.'))
