from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django_apscheduler.jobstores import DjangoJobStore,register_events
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    ema_scheduler = BackgroundScheduler()
    ema_scheduler.add_jobstore(DjangoJobStore(), "default")

    ema_scheduler.add_job(
        run_ema5_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="ema5_calculation",
        replace_existing=True
    )
    ema_scheduler.add_job(
        run_ema10_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="ema10_calculation",
        replace_existing=True
    )
    ema_scheduler.add_job(
        run_ema20_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="ema20_calculation",
        replace_existing=True
    )
    ema_scheduler.add_job(
        run_ema30_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="ema30_calculation",
        replace_existing=True
    )
    ema_scheduler.add_job(
        run_ema50_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="ema50_calculation",
        replace_existing=True
    )
    ema_scheduler.add_job(
        run_ema100_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="ema100_calculation",
        replace_existing=True
    )
    ema_scheduler.add_job(
        run_ema200_calculation,
        trigger=IntervalTrigger(minutes=1),
        id="ema200_calculation",
        replace_existing=True
    )
    register_events(ema_scheduler)
    ema_scheduler.start()

    logger.info("Scheduler started for ema detection.")

def stop_scheduler():
    """
    Stops the APScheduler.
    """
    ema_scheduler = BackgroundScheduler()
    if ema_scheduler.running:
        ema_scheduler.remove_all_jobs()  # Remove all scheduled jobs
        ema_scheduler.shutdown(wait=False)  # Gracefully shut down the scheduler
        print("Scheduler stopped for emas.")

def run_ema5_calculation():
    try:
        call_command('ema5')  # Replace with your actual command name
        logger.info("Detect emas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_ema10_calculation():
    try:
        call_command('ema10')  # Replace with your actual command name
        logger.info("Detect emas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_ema20_calculation():
    try:
        call_command('ema20')  # Replace with your actual command name
        logger.info("Detect emas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_ema30_calculation():
    try:
        call_command('ema30')  # Replace with your actual command name
        logger.info("Detect emas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_ema50_calculation():
    try:
        call_command('ema50')  # Replace with your actual command name
        logger.info("Detect emas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_ema100_calculation():
    try:
        call_command('ema100')  # Replace with your actual command name
        logger.info("Detect emas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")

def run_ema200_calculation():
    try:
        call_command('ema200')  # Replace with your actual command name
        logger.info("Detect emas calculation command executed successfully.")
    except Exception as e:
        logger.error(f"Error running Detect Calculation calculation: {e}")