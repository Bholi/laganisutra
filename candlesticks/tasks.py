from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore,register_events
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    candle_scheduler = BackgroundScheduler()
    candle_scheduler.add_jobstore(DjangoJobStore(), "default")

    candle_scheduler.add_job(
        run_detect_candles_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="detect_candles_calculation",
        replace_existing=True
    )
    register_events(candle_scheduler)
    candle_scheduler.start()

    logger.info("Scheduler started for candle detection.")

def stop_scheduler():
    """
    Stops the APScheduler.
    """
    scheduler = BackgroundScheduler()
    if scheduler.running:
        scheduler.remove_all_jobs()  # Remove all scheduled jobs
        scheduler.shutdown(wait=False)  # Gracefully shut down the scheduler
        print("Scheduler stopped for candles.")

def run_detect_candles_calculation():
    try:
        call_command('detect_candles')  # Replace with your actual command name
        logger.info("Detect Candles calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")