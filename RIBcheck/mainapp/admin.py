from django.contrib import admin
from .models import CustomUser, LogEntry

admin.site.register(CustomUser)
admin.site.register(LogEntry)