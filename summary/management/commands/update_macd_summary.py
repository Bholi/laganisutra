from django.core.management.base import BaseCommand

from summary.views import update_macd_summary

class Command(BaseCommand):
    help = 'Update the MACD Summary table'

    def handle(self, *args, **kwargs):
        update_macd_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated MACD Summary'))
