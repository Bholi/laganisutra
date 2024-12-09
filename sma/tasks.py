from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore,register_events
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    sma_scheduler = BackgroundScheduler()
    sma_scheduler.add_jobstore(DjangoJobStore(), "default")

    sma_scheduler.add_job(
        run_sma5_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="sma5_calculation",
        replace_existing=True
    )
    sma_scheduler.add_job(
        run_sma10_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="sma10_calculation",
        replace_existing=True
    )
    sma_scheduler.add_job(
        run_sma20_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="sma20_calculation",
        replace_existing=True
    )
    sma_scheduler.add_job(
        run_sma30_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="sma30_calculation",
        replace_existing=True
    )
    sma_scheduler.add_job(
        run_sma50_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="sma50_calculation",
        replace_existing=True
    )
    sma_scheduler.add_job(
        run_sma100_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="sma100_calculation",
        replace_existing=True
    )
    sma_scheduler.add_job(
        run_sma200_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="sma200_calculation",
        replace_existing=True
    )
    register_events(sma_scheduler)
    sma_scheduler.start()

    logger.info("Scheduler started for sma detection.")

def stop_scheduler():
    """
    Stops the APScheduler.
    """
    sma_scheduler = BackgroundScheduler()
    if sma_scheduler.running:
        sma_scheduler.remove_all_jobs()  # Remove all scheduled jobs
        sma_scheduler.shutdown(wait=False)  # Gracefully shut down the scheduler
        print("Scheduler stopped for smas.")

def run_sma5_calculation():
    try:
        call_command('sma5')  # Replace with your actual command name
        logger.info("Detect smas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_sma10_calculation():
    try:
        call_command('sma10')  # Replace with your actual command name
        logger.info("Detect smas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_sma20_calculation():
    try:
        call_command('sma20')  # Replace with your actual command name
        logger.info("Detect smas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_sma30_calculation():
    try:
        call_command('sma30')  # Replace with your actual command name
        logger.info("Detect smas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_sma50_calculation():
    try:
        call_command('sma50')  # Replace with your actual command name
        logger.info("Detect smas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_sma100_calculation():
    try:
        call_command('sma100')  # Replace with your actual command name
        logger.info("Detect smas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_sma200_calculation():
    try:
        call_command('sma200')  # Replace with your actual command name
        logger.info("Detect smas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")