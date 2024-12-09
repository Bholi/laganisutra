# detect_embezzlement.py

import pandas as pd
from django.core.management.base import BaseCommand
from manupulation.models import EmbezzlementData

class Command(BaseCommand):
    help = 'Detect embezzlement from floorsheet data'

    def handle(self, *args, **kwargs):
        # Load the floorsheet data
        file_path = "/Users/faizansari/Downloads/analysis/scrapper/data/floorsheet_data.csv"
        df = pd.read_csv(file_path)

        # Convert 'Rate' and 'Quantity' to numeric, cleaning any commas if present
        df['Rate'] = pd.to_numeric(df['Rate'].str.replace(',', ''), errors='coerce')
        df['Quantity'] = pd.to_numeric(df['Quantity'].str.replace(',', ''), errors='coerce')

        # Initialize columns for embezzlement detection
        df['EmbezzlementFlag'] = False

        # Threshold for detecting unusual transactions
        unusual_transaction_threshold = 10000  # Example threshold for large transactions

        # Detect Unusual Transactions
        mean_amounts = df.groupby('Buyer')['Rate'].mean()
        df['UnusualTransactionFlag'] = df.apply(
            lambda row: row['Rate'] > mean_amounts[row['Buyer']] + unusual_transaction_threshold,
            axis=1
        )

        # Update the EmbezzlementFlag for unusual transactions
        df['EmbezzlementFlag'] |= df['UnusualTransactionFlag']

        # Detect Frequent Changes in Buyer/Seller Information
        buyer_changes = df.groupby('Transact. No.')['Buyer'].nunique()
        seller_changes = df.groupby('Transact. No.')['Seller'].nunique()

        df['FrequentBuyerChangeFlag'] = df['Transact. No.'].isin(buyer_changes[buyer_changes > 1].index)
        df['FrequentSellerChangeFlag'] = df['Transact. No.'].isin(seller_changes[seller_changes > 1].index)

        # Update the EmbezzlementFlag for frequent changes
        df['EmbezzlementFlag'] |= df['FrequentBuyerChangeFlag'] | df['FrequentSellerChangeFlag']

        # Prepare the output DataFrame
        output_df = df[['Transact. No.', 'Symbol', 'Buyer', 'Seller', 'Rate', 'Quantity', 'EmbezzlementFlag']]
        output_df.columns = ['transaction_no', 'symbol', 'buyer', 'seller', 'price', 'volume', 'embezzlement_flag']

        # Save the output to the database
        for _, row in output_df.iterrows():
            EmbezzlementData.objects.update_or_create(
                transaction_no=row['transaction_no'],
                symbol=row['symbol'],
                buyer=row['buyer'],
                seller=row['seller'],
                price=row['price'],
                volume=row['volume'],
                embezzlement_flag=row['embezzlement_flag']
            )

        self.stdout.write(self.style.SUCCESS('Embezzlement detection completed successfully.'))
