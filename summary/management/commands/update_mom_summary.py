from django.core.management.base import BaseCommand

from summary.views import update_mom_summary

class Command(BaseCommand):
    help = 'Update the MOM Summary table'

    def handle(self, *args, **kwargs):
        update_mom_summary()
        self.stdout.write(self.style.SUCCESS('Successfully updated MOM Summary'))
