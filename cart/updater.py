from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .job import restock


def start():
    """
    Scheduling for restock function
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(restock, 'interval', minutes=15)
    scheduler.start()
