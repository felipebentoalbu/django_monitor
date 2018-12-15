from apscheduler.schedulers.blocking import BlockingScheduler
from module_monitor.models import Monitor

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minute.')
    Monitor.toMonitor()

sched.start()