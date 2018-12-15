"""django_monitor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('module_monitor.urls')),
]

# from module_monitor.views import toMonitor
# from time import sleep
# from decouple import config 
# import threading

# t = threading.Thread(target=toMonitor,args=("thread sendo executada",))
# t.start()
# while t.isAlive():
#     print("Aguardando thread")
#     sleep(int(config("SLEEP_TIME")))