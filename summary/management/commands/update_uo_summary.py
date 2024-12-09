from django.core.management.base import BaseCommand

from summary.views import update_uo_summary

class Command(BaseCommand):
    help = 'Update the UO Summary table'

    def handle(self, *args, **kwargs):
        update_uo_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated UO Summary'))
