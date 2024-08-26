# Generated by Django 4.2.1 on 2024-03-05 14:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_customuser_salt_alter_customuser_signature'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('message', models.TextField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mainapp_logentries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
