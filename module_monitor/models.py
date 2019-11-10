from django.db import models

# Create your models here.

class Monitor(models.Model):
    host = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    status_code = models.CharField(max_length=100)
    current_status_code = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_execution = models.DateTimeField(null=True)
    last_trouble = models.DateTimeField(null=True)
    status = models.BooleanField(null=True)
    is_online = models.BooleanField(null=True)

    def __str__(self):
        return self.name