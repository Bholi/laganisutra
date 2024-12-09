import datetime
from django.core.management.base import BaseCommand
from livedata.models import LiveFeedData
from stages.models import MarketCycleStage

class Command(BaseCommand):
    help = 'Calculate and store stock market cycle stages'

    def handle(self, *args, **kwargs):
        # Fetch all LiveFeedData entries
        data = LiveFeedData.objects.all()

        for record in data:
            symbol = record.symbol
            ltp = self.clean_and_convert_to_float(record.ltp)
            high = self.clean_and_convert_to_float(record.high)
            low = self.clean_and_convert_to_float(record.low)
            open_price = self.clean_and_convert_to_float(record.open)
            previous_close = self.clean_and_convert_to_float(record.previous_closing)
            volume = self.clean_and_convert_to_float(record.volume)

            if not all([ltp, high, low, open_price, previous_close, volume]):
                # Skip records with insufficient or invalid data
                continue

            # Determine the market cycle stage
            stage = self.determine_stage(ltp, high, low, open_price, previous_close, volume)

            # Store the result in MarketCycleStage
            MarketCycleStage.objects.create(
                symbol=symbol,
                stage=stage,
                date=record.datetime.date() if record.datetime else datetime.date.today()
            )

            self.stdout.write(f'Successfully processed symbol {symbol} with stage {stage}')

    def clean_and_convert_to_float(self, value):
        """
        Clean a string value by removing commas and converting to float.
        """
        try:
            if value is not None:
                # Remove commas and convert to float
                return float(value.replace(',', ''))
            return None
        except ValueError:
            return None

    def determine_stage(self, ltp, high, low, open_price, previous_close, volume):
        """
        Determine the stock market cycle stage based on the data.
        """
        # Example logic for determining stages (this is a simplified example):
        if ltp > previous_close and volume > 1.5 * ((high - low) / previous_close):
            return "Markup"
        elif ltp < previous_close and volume < 0.8 * ((high - low) / previous_close):
            return "Markdown"
        elif ltp > open_price and ltp < high * 0.9:
            return "Accumulation"
        elif ltp < open_price and ltp > low * 1.1:
            return "Distribution"
        else:
            return "Unknown"
