from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models.functions import Length

from .models import Monitor


@staff_member_required
def home(request):
    servers = Monitor.objects.all().order_by(Length('is_online').asc())
    return render(request, 'home.html',{'servers': servers})