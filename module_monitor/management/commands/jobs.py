from apscheduler.schedulers.blocking import BlockingScheduler
from django.core.management.base import BaseCommand
from module_monitor.models import Monitor

class Command(BaseCommand):
    sched = BlockingScheduler()

    @sched.scheduled_job('interval', minutes=1)
    def timed_job():
        print('This job is run every one minute.')
        Monitor.toMonitor()

    sched.start()