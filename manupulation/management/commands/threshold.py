# threshold_tuning.py

import pandas as pd
from django.core.management.base import BaseCommand
from manupulation.models import ThresholdTuningData

class Command(BaseCommand):
    help = 'Detect anomalies through threshold tuning from floorsheet data'

    def handle(self, *args, **kwargs):
        # Load the floorsheet data
        file_path = "/Users/faizansari/Downloads/analysis/scrapper/data/floorsheet_data.csv"
        df = pd.read_csv(file_path)

        # Convert 'Rate' and 'Quantity' to numeric, cleaning commas if present
        df['Rate'] = pd.to_numeric(df['Rate'].str.replace(',', ''), errors='coerce')
        df['Quantity'] = pd.to_numeric(df['Quantity'].str.replace(',', ''), errors='coerce')

        # Define thresholds
        high_value_threshold = 10000
        low_value_threshold = 100

        # Initialize flags
        df['HighValueTransactionFlag'] = df['Rate'] > high_value_threshold
        df['LowValueTransactionFlag'] = df['Rate'] < low_value_threshold

        # Analyze buyers' transaction counts
        transaction_counts = df['Buyer'].value_counts()
        avg_transactions = transaction_counts.mean()
        std_transactions = transaction_counts.std()

        # Calculate thresholds based on standard deviations
        high_transaction_threshold = avg_transactions + std_transactions
        low_transaction_threshold = avg_transactions - std_transactions

        # Flag buyers based on tuned thresholds
        df['FrequentBuyerFlag'] = df['Buyer'].isin(transaction_counts[transaction_counts > high_transaction_threshold].index)
        df['RareBuyerFlag'] = df['Buyer'].isin(transaction_counts[transaction_counts < low_transaction_threshold].index)

        # Aggregate flags to identify potential anomalies
        df['PotentialAnomaly'] = (
            df['HighValueTransactionFlag'] | 
            df['LowValueTransactionFlag'] | 
            df['FrequentBuyerFlag'] | 
            df['RareBuyerFlag']
        )

        # Prepare the DataFrame for saving to the database
        output_df = df[['Transact. No.', 'Symbol', 'Buyer', 'Seller', 'Rate', 'Quantity',
                        'HighValueTransactionFlag', 'LowValueTransactionFlag', 
                        'FrequentBuyerFlag', 'RareBuyerFlag', 'PotentialAnomaly']]
        output_df.columns = [
            'transaction_no', 'symbol', 'buyer', 'seller', 'price', 'volume', 
            'high_value_flag', 'low_value_flag', 'frequent_buyer_flag', 
            'rare_buyer_flag', 'potential_anomaly'
        ]

        # Save the data to the database
        for _, row in output_df.iterrows():
            ThresholdTuningData.objects.update_or_create(
                transaction_no=row['transaction_no'],
                defaults={
                    'symbol': row['symbol'],
                    'buyer': row['buyer'],
                    'seller': row['seller'],
                    'price': row['price'],
                    'volume': row['volume'],
                    'high_value_flag': row['high_value_flag'],
                    'low_value_flag': row['low_value_flag'],
                    'frequent_buyer_flag': row['frequent_buyer_flag'],
                    'rare_buyer_flag': row['rare_buyer_flag'],
                    'potential_anomaly': row['potential_anomaly']
                }
            )

        self.stdout.write(self.style.SUCCESS('Threshold tuning detection completed successfully.'))
