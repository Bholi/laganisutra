from django.core.management.base import BaseCommand

from summary.views import update_adx_summary

class Command(BaseCommand):
    help = 'Update the ADX Summary table'

    def handle(self, *args, **kwargs):
        update_adx_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated ADX Summary'))
