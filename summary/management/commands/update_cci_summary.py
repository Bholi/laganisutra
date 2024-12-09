from django.core.management.base import BaseCommand

from summary.views import update_cci_summary

class Command(BaseCommand):
    help = 'Update the CCI Summary table'

    def handle(self, *args, **kwargs):
        update_cci_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated CCI Summary'))
