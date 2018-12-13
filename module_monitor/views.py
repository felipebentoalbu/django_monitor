from django.shortcuts import render
from .models import Monitor

from time import sleep
from decouple import config
import smtplib
import requests

from django.contrib.admin.views.decorators import staff_member_required

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
                    # atualizar info is_online
                    obj_update = Monitor.objects.get(id=server.id)
                    obj_update.is_online = False
                    obj_update.save()
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


@staff_member_required
def home(request):
    servers = Monitor.objects.all()
    return render(request, 'home.html',{'servers': servers})