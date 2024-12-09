from django.core.management.base import BaseCommand

from summary.views import update_bop_summary

class Command(BaseCommand):
    help = 'Update the BOP Summary table'

    def handle(self, *args, **kwargs):
        update_bop_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated BOP Summary'))
