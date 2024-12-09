from django.core.management.base import BaseCommand

from summary.views import update_stoch_summary

class Command(BaseCommand):
    help = 'Update the Stoch Summary table'

    def handle(self, *args, **kwargs):
        update_stoch_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated Stoch Summary'))
