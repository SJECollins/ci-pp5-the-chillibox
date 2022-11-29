from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .job import restock


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(restock, 'interval', minutes=2)
    scheduler.start()
