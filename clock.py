from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()

sched.add_job(timed_job, 'interval', minutes=1, id='my_job_id')
def timed_job():
    print('This job is run every three minutes.')

sched.start()