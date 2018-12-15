from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
import threading
from time import sleep
import smtplib
import requests
from module_monitor.models import Monitor

def toMonitor():

    while True:
        sleep(int(config("SLEEP_TIME")))
        servers = Monitor.objects.all()
        if not servers:
            print("Sem serviços cadastrados para o monitoramento.")
        else:
            for server in servers:
                r = requests.get(server.host)
                print(str(r.status_code) + " - " + server.name + " - " + server.host)
                if(server.status_code != str(r.status_code)):
                    send_email(server, r.status_code)  

def send_email(server, status_code):
    
    TO = server.email
    SUBJECT = '(' + str(status_code) + ')' + ' - unavailable service - ' + server.name
    TEXT = 'Servico esta indisponivel!\nName:{NAME} Host: {HOST}\nStatus code esperado: {STATUS_ORIGINAL}\nStatus code atual:{STATUS_CURRENT}'.format(
        NAME=server.name,
        HOST=server.host,
        STATUS_ORIGINAL=server.status_code,
        STATUS_CURRENT=status_code
    )

    # Gmail Sign In
    gmail_sender = config("SENDER_EMAIL")
    gmail_passwd = config("PASS_EMAIL")

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(gmail_sender, gmail_passwd)

    BODY = '\r\n'.join(['To: %s' % TO,
                        'From: %s' % gmail_sender,
                        'Subject: %s' % SUBJECT,
                        '', TEXT])

    try:
        server.sendmail(gmail_sender, [TO], BODY)
        print ('email sent')
    except:
        print ('error sending mail')

    server.quit()

class Command(BaseCommand):

    def handle(self, *args, **options):
        t = threading.Thread(target=toMonitor)
        t.start()

    # sched = BackgroundScheduler()
    # sched.add_job(toMonitor(), 'interval', minutes=1)
    # sched.start()

# if __name__ == '__main__':
#     Command()