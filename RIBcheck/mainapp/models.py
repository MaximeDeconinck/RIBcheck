from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    adress = models.CharField(max_length=255)
    country = models.CharField(max_length=3)
    iban = models.CharField(max_length=27, blank=True, null=True)
    signature = models.CharField(max_length=128)
    salt = models.CharField(max_length=16)

    def __str__(self):
        return self.username

class LogEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='mainapp_logentries')
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField()