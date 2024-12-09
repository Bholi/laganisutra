from django.core.management.base import BaseCommand

from summary.views import update_vwma_summary

class Command(BaseCommand):
    help = 'Update the VMWA Summary table'

    def handle(self, *args, **kwargs):
        update_vwma_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated VWMA Summary'))
