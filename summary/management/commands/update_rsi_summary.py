from django.core.management.base import BaseCommand

from summary.views import update_rsi_summary

class Command(BaseCommand):
    help = 'Update the RSI Summary table'

    def handle(self, *args, **kwargs):
        update_rsi_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated RSI Summary'))
