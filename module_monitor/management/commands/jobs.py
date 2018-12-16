from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from decouple import config
import threading
from time import sleep
import requests
from module_monitor.models import Monitor
from datetime import datetime
from django import db

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def toMonitor():

    while True:

        sleep(int(config("SLEEP_TIME")))
        servers = Monitor.objects.all()
        if not servers:
            print("Sem serviços cadastrados para o monitoramento.")
        else:
            for server in servers:
                sleep(int(config("SLEEP_TIME_REQ")))
                r = requests.get(server.host)
                print(str(r.status_code) + " - " + server.name + " - " + server.host)

                if server.status:
                    if server.status_code != str(r.status_code):
                        if server.is_online == True:
                            send_email(server, r.status_code, False)
                        Monitor.objects.filter(id=server.id).update(current_status_code=str(r.status_code), is_online=False, last_trouble=datetime.now())
                    else:
                        if server.is_online == False:
                            send_email(server, r.status_code, True)
                            Monitor.objects.filter(id=server.id).update(current_status_code=str(r.status_code), is_online=True)
                        if server.current_status_code != str(r.status_code):
                            Monitor.objects.filter(id=server.id).update(current_status_code=str(r.status_code))
        db.connections.close_all()

def send_email(server_info, status_code, is_online):

    if is_online:
        text_is_online = "disponível novamente"
    else:
        text_is_online = "indisponível"

    gmailUser = config("SENDER_EMAIL")
    gmailPassword = config("PASS_EMAIL")
    recipient = server_info.email
    message= 'Serviço está ' + text_is_online + '.\nName: {NAME} Host: {HOST}\nStatus code esperado: {STATUS_ORIGINAL}\nStatus code atual: {STATUS_CURRENT}\nData do problema: {LAST_TROUBLE}'.format(
        NAME=server_info.name,
        HOST=server_info.host,
        STATUS_ORIGINAL=server_info.status_code,
        STATUS_CURRENT=status_code,
        LAST_TROUBLE=server_info.last_trouble
    )

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = '(' + str(status_code) + ' - ' + server_info.name + ')' + ' - Serviço está ' + text_is_online
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)
    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    mailServer.close()

class Command(BaseCommand):

    def handle(self, *args, **options):
        t = threading.Thread(target=toMonitor)
        t.start()
