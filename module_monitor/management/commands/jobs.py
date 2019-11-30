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
import urllib3

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def toMonitor():
    print("[START] Inicializando monitoramento dos serviços...")    
    while True:
        servers = Monitor.objects.all()
        if not servers:
            print("Sem serviços cadastrados para o monitoramento.")
        else:
            for server in servers:
                print("[WAIT] Aguardando timeout... " + config("SLEEP_TIME") + "s")
                sleep(int(config("SLEEP_TIME")))
                print("******************************START_MONITORING******************************")
                # Apenas monitora o serviço se o status estiver habilitado ('True')
                if server.status:
                    try:
                        r = requests.get(server.host, timeout=30, verify=False)
                        request_status_code =  str(r.status_code)
                    except:
                        request_status_code = str(521)
                    print("[{SERVER_NAME}] Serviço monitorado... {SERVER_HOST} | Status Code... Atual: [{CODE_ATUAL}] Aguardado: [{CODE_AGUARDADO}]".format(
                        CODE_AGUARDADO=server.status_code,
                        CODE_ATUAL=str(request_status_code),
                        SERVER_NAME=server.name,
                        SERVER_HOST=server.host
                    ))
                    print("[ONLINE] Serviço disponível..." if server.status_code == request_status_code else "[OFFLINE] Serviço indisponível...")
                    # Verifica se o status code é diferente do atual
                    send_notification = server.current_status_code != request_status_code
                    print("[E-MAIL] Enviando notificação..." if send_notification else "[E-MAIL] Sem notificação para ser enviado...")
                    # Atualizando última execução
                    Monitor.objects.filter(id=server.id).update(last_execution=datetime.now())
                    if server.status:
                        # Envia e-mail caso sistema esteja online e recebe status code diferente ao aguardado
                        if  send_notification and server.is_online:
                            print("[ON] Serviço online")
                            Monitor.objects.filter(id=server.id).update(current_status_code=request_status_code, is_online=False, last_trouble=datetime.now())
                            send_email(server, request_status_code, False)
                        # Envia e-mail caso sistema esteja offline e recebe status code igual ao aguardado
                        elif send_notification and server.is_online == False:
                            print("[OFF] Serviço offline")
                            Monitor.objects.filter(id=server.id).update(current_status_code=request_status_code, is_online=True)
                            send_email(server, request_status_code, True)
                        else:
                            # Atualiza status code atual (request_status_code)
                            print("[OK] Nenhuma mudança de status code")
                            Monitor.objects.filter(id=server.id).update(current_status_code=request_status_code)
                print("******************************FINAL_MONITORING******************************")
        db.connections.close_all()

def send_email(server_info, request_status_code, is_online):
    print("[" + server_info.name + "] Enviando notificação via e-mail...")
    if is_online:
        text_is_online = "disponível novamente"
    else:
        text_is_online = "indisponível"

    gmailUser = config("SENDER_EMAIL")
    gmailPassword = config("PASS_EMAIL")
    recipient = server_info.email
    message= 'Serviço está ' + text_is_online + '.\nName: {NAME}\nHost: {HOST}\nStatus code esperado: {STATUS_ORIGINAL}\nStatus code atual: {STATUS_CURRENT}\nData do último problema: {LAST_TROUBLE}'.format(
        NAME=server_info.name,
        HOST=server_info.host,
        STATUS_ORIGINAL=server_info.status_code,
        STATUS_CURRENT=request_status_code,
        LAST_TROUBLE=server_info.last_trouble
    )

    msg = MIMEMultipart()
    msg['From'] = gmailUser
    msg['To'] = recipient
    msg['Subject'] = '[' + request_status_code + '] - ' + server_info.name + ' - Serviço está ' + text_is_online
    msg.attach(MIMEText(message))

    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmailUser, gmailPassword)

    print("[E-MAIL] Enviando para... " + recipient)
    print("[TEMPLATE] " + message)

    mailServer.sendmail(gmailUser, recipient, msg.as_string())
    print("[E-MAIL] Enviado com sucesso... " + recipient)
    mailServer.close()

class Command(BaseCommand):

    def handle(self, *args, **options):
        t = threading.Thread(target=toMonitor)
        t.start()
