from django.db import models

# Create your models here.

class Monitor(models.Model):
    host = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    status_code = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(null=True, blank=True)
    is_online = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name