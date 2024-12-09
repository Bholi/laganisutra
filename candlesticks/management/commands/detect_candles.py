import pandas as pd
from django.core.management.base import BaseCommand
from candlesticks.detecting_logic import detect_candlestick_patterns


class Command(BaseCommand):
    help = 'Detect candlestick patterns and store results in the database'

    def handle(self, *args, **kwargs):
        detect_candlestick_patterns()
        self.stdout.write(self.style.SUCCESS('Successfully detected candlestick patterns and saved them.'))
