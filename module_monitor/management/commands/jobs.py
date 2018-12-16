from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
import threading
from time import sleep
import smtplib
import requests
from module_monitor.models import Monitor
from datetime import datetime
from django import db

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

                if server.status_code != str(r.status_code):
                    if server.is_online == True:
                        send_email(server, r.status_code, False)
                    Monitor.objects.filter(id=server.id).update(current_status_code=str(r.status_code), is_online=False, last_trouble=datetime.now())
                else:
                    if server.is_online == False:
                        send_email(server, r.status_code, True)
                        Monitor.objects.filter(id=server.id).update(current_status_code=str(r.status_code), is_online=True)
        db.connections.close_all()

def send_email(server, status_code, is_online):
    
    TO = server.email
    if(is_online):
        text_is_online = "disponível novamente"
    else:
        text_is_online = "indisponível"
    SUBJECT = '(' + str(status_code) + ')' + ' - servico esta ' + text_is_online + ' - ' + server.name
    TEXT = 'Servico esta ' + text_is_online + '.\nName:{NAME} Host: {HOST}\nStatus code esperado: {STATUS_ORIGINAL}\nStatus code atual:{STATUS_CURRENT}'.format(
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
