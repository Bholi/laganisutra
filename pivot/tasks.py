from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore,register_events
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    pivot_scheduler = BackgroundScheduler()
    pivot_scheduler.add_jobstore(DjangoJobStore(), "default")

    pivot_scheduler.add_job(
        run_standard_pivot_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="pivot_calculation",
        replace_existing=True
    )
    pivot_scheduler.add_job(
        run_camrilla_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="camrilla_calculation",
        replace_existing=True
    )
    pivot_scheduler.add_job(
        run_fibo_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="fibo_calculation",
        replace_existing=True
    )
    register_events(pivot_scheduler)
    pivot_scheduler.start()

    logger.info("Scheduler started for pivot detection.")

def stop_scheduler():
    """
    Stops the APScheduler.
    """
    pivot_scheduler = BackgroundScheduler()
    if pivot_scheduler.running:
        pivot_scheduler.remove_all_jobs()  # Remove all scheduled jobs
        pivot_scheduler.shutdown(wait=False)  # Gracefully shut down the scheduler
        print("Scheduler stopped for pivots.")

def run_standard_pivot_calculation():
    try:
        call_command('pivot')  # Replace with your actual command name
        logger.info("Detect pivot calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Pivot Calculation calculation: {e}")

def run_camrilla_calculation():
    try:
        call_command('camrilla')  # Replace with your actual command name
        logger.info("Detect Camrilla calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Camrilla Calculation calculation: {e}")

def run_fibo_calculation():
    try:
        call_command('fibo')  # Replace with your actual command name
        logger.info("Detect Fibo calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Fibo Calculation calculation: {e}")