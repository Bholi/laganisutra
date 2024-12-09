from django.core.management.base import BaseCommand

from summary.views import update_ao_summary

class Command(BaseCommand):
    help = 'Update the AO Summary table'

    def handle(self, *args, **kwargs):
        update_ao_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated AO Summary'))
