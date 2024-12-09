from django.core.management.base import BaseCommand

from summary.views import update_willr_summary

class Command(BaseCommand):
    help = 'Update the WillR Summary table'

    def handle(self, *args, **kwargs):
        update_willr_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated WIllR Summary'))
