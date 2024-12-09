# # analyze_trades.py

# import pandas as pd
# from django.core.management.base import BaseCommand
# from manupulation.models import TradeAnalysis

# class Command(BaseCommand):
#     help = 'Analyze trade data and store results in the database'

#     def handle(self, *args, **kwargs):
#         # Load real data from a CSV file
#         file_path = '/Users/faizansari/Downloads/analysis/scrapper/data/floorsheet_data.csv'
#         df = pd.read_csv(file_path)

#         # Convert 'Rate' and 'Quantity' to numeric, coerce errors to NaN
#         df['Rate'] = pd.to_numeric(df['Rate'], errors='coerce')
#         df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

#         unique_symbols = df['Symbol'].unique()
        
#         for symbol in unique_symbols:
#             symbol_df = df[df['Symbol'] == symbol].copy()

#             # Analyze the trades
#             repeated_trades = symbol_df.groupby(['Buyer', 'Seller']).size().reset_index(name='TradeCount')
#             symbol_df['RepeatedTradesFlag'] = symbol_df.duplicated(['Buyer', 'Seller'], keep=False)

#             symbol_df['RateChange'] = symbol_df['Rate'].pct_change()
#             symbol_df['PriceManipulationFlag'] = symbol_df['RateChange'].abs() > 0.05
#             symbol_df['PaintingTheTapeFlag'] = (symbol_df['Quantity'] < 10) & (symbol_df['RateChange'].abs() > 0.03)
#             symbol_df['AverageQuantity'] = symbol_df['Quantity'].mean(skipna=True)
#             symbol_df['VolumeSpikeFlag'] = symbol_df['Quantity'] > 2 * symbol_df['AverageQuantity']
#             circular_trades = symbol_df[
#                 (symbol_df['Buyer'] == symbol_df['Seller'].shift(-1)) &
#                 (symbol_df['Seller'] == symbol_df['Buyer'].shift(-1))
#             ]
#             symbol_df['CircularTradingFlag'] = symbol_df.index.isin(circular_trades.index)
#             symbol_df['PumpFlag'] = symbol_df['RateChange'] > 0.1
#             symbol_df['DumpFlag'] = symbol_df['RateChange'] < -0.1
#             symbol_df['PumpAndDumpFlag'] = symbol_df['PumpFlag'] & symbol_df['DumpFlag'].shift(-1)
#             symbol_df['SellerReappearsFlag'] = symbol_df['Seller'].duplicated(keep=False)
#             symbol_df['Suspicious'] = symbol_df[
#                 ['RepeatedTradesFlag', 'PriceManipulationFlag', 'PaintingTheTapeFlag',
#                  'VolumeSpikeFlag', 'CircularTradingFlag', 'PumpAndDumpFlag', 
#                  'SellerReappearsFlag']
#             ].any(axis=1)

#             # Save results to the database
#             for _, row in symbol_df.iterrows():
#                 TradeAnalysis.objects.create(
#                     transact_no=row['Transact. No.'],
#                     symbol=row['Symbol'],
#                     buyer=row['Buyer'],
#                     seller=row['Seller'],
#                     repeated_trades_flag=row['RepeatedTradesFlag'],
#                     price_manipulation_flag=row['PriceManipulationFlag'],
#                     painting_the_tape_flag=row['PaintingTheTapeFlag'],
#                     volume_spike_flag=row['VolumeSpikeFlag'],
#                     circular_trading_flag=row['CircularTradingFlag'],
#                     pump_flag=row['PumpFlag'],
#                     dump_flag=row['DumpFlag'],
#                     seller_reappears_flag=row['SellerReappearsFlag'],
#                     suspicious=row['Suspicious'],
#                 )
#         self.stdout.write(self.style.SUCCESS('Trade analysis complete and data saved.'))

import pandas as pd
import requests
from django.core.management.base import BaseCommand
from manupulation.models import TradeAnalysis
from django.db import transaction

class Command(BaseCommand):
    help = 'Analyze trade data and store results in the database'

    def handle(self, *args, **kwargs):
        # Fetch data from the API
        api_url = 'https://tvapi.volcussoft.com/api/floorsheet/'
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            # Convert columns to appropriate data types
            df['rate'] = pd.to_numeric(df['rate'], errors='coerce')
            df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')

            unique_symbols = df['symbol'].unique()

            for symbol in unique_symbols:
                symbol_df = df[df['symbol'] == symbol].copy()

                # Analyze the trades
                repeated_trades = symbol_df.groupby(['buyer', 'seller']).size().reset_index(name='TradeCount')
                symbol_df['RepeatedTradesFlag'] = symbol_df.duplicated(['buyer', 'seller'], keep=False)

                symbol_df['RateChange'] = symbol_df['rate'].pct_change()
                symbol_df['PriceManipulationFlag'] = symbol_df['RateChange'].abs() > 0.05
                symbol_df['PaintingTheTapeFlag'] = (symbol_df['quantity'] < 10) & (symbol_df['RateChange'].abs() > 0.03)
                symbol_df['AverageQuantity'] = symbol_df['quantity'].mean(skipna=True)
                symbol_df['VolumeSpikeFlag'] = symbol_df['quantity'] > 2 * symbol_df['AverageQuantity']
                circular_trades = symbol_df[
                    (symbol_df['buyer'] == symbol_df['seller'].shift(-1)) &
                    (symbol_df['seller'] == symbol_df['buyer'].shift(-1))
                ]
                symbol_df['CircularTradingFlag'] = symbol_df.index.isin(circular_trades.index)
                symbol_df['PumpFlag'] = symbol_df['RateChange'] > 0.1
                symbol_df['DumpFlag'] = symbol_df['RateChange'] < -0.1
                symbol_df['PumpAndDumpFlag'] = symbol_df['PumpFlag'] & symbol_df['DumpFlag'].shift(-1)
                symbol_df['SellerReappearsFlag'] = symbol_df['seller'].duplicated(keep=False)
                symbol_df['Suspicious'] = symbol_df[
                    ['RepeatedTradesFlag', 'PriceManipulationFlag', 'PaintingTheTapeFlag',
                     'VolumeSpikeFlag', 'CircularTradingFlag', 'PumpAndDumpFlag', 
                     'SellerReappearsFlag']
                ].any(axis=1)

                with transaction.atomic():
                    # Save results to the database
                    for _, row in symbol_df.iterrows():
                        TradeAnalysis.objects.create(
                            transact_no=row['transaction_no'],
                            symbol=row['symbol'],
                            buyer=row['buyer'],
                            seller=row['seller'],
                            repeated_trades_flag=row['RepeatedTradesFlag'],
                            price_manipulation_flag=row['PriceManipulationFlag'],
                            painting_the_tape_flag=row['PaintingTheTapeFlag'],
                            volume_spike_flag=row['VolumeSpikeFlag'],
                            circular_trading_flag=row['CircularTradingFlag'],
                            pump_flag=row['PumpFlag'],
                            dump_flag=row['DumpFlag'],
                            seller_reappears_flag=row['SellerReappearsFlag'],
                            suspicious=row['Suspicious'],
                        )
            self.stdout.write(self.style.SUCCESS('Trade analysis complete and data saved.'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch data from the API.'))
