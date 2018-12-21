from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from .models import Monitor


@staff_member_required
def home(request):
    servers = Monitor.objects.all().order_by('-is_online', '-last_execution', '-status')
    return render(request, 'home.html',{'servers': servers})