from django.apps import AppConfig
from django.utils.timezone import localtime
import threading
import time
import os

class EmaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ema'

    # scheduler_running = False
    # def ready(self):
    #     if os.environ.get('RUN_MAIN')=='true':
    #         from ema.tasks import start_scheduler, stop_scheduler

    #         def manage_scheduler():
    #             """
    #             Starts the scheduler during the allowed time range and stops it outside the range.
    #             """
    #             while True:
    #                 current_time = localtime().time()
    #                 start_time = localtime().replace(hour=11, minute=0, second=0, microsecond=0).time()
    #                 cutoff_time = localtime().replace(hour=15, minute=0, second=0, microsecond=0).time()

    #                 if start_time <= current_time < cutoff_time:
    #                     if not self.scheduler_running:
    #                         try:
    #                             start_scheduler()
    #                             self.scheduler_running = True
    #                             print("Scheduler started for candles.")
    #                         except Exception as e:
    #                             print(f"Failed to start scheduler for candles: {e}")
    #                 else:
    #                     if self.scheduler_running:
    #                         try:
    #                             stop_scheduler()
    #                             self.scheduler_running = False
    #                             print("Scheduler stopped.")
    #                         except Exception as e:
    #                             print(f"Failed to stop scheduler: {e}")

    #                 # Wait for 60 seconds before checking again
    #                 time.sleep(60)

    #         # Start the thread for managing the scheduler
    #         threading.Thread(target=manage_scheduler, daemon=True).start()
