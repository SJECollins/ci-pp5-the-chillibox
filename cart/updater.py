from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .job import restock


def start():
    """
    Scheduling for restock function
    Based on https://www.youtube.com/watch?v=Lzy4G1wZ7NQ&ab_channel=DidCoding
    """
    scheduler = BackgroundScheduler()
    scheduler.add_job(restock, 'interval', minutes=15)
    scheduler.start()
