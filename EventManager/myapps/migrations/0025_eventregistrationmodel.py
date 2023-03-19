# Generated by Django 4.1.7 on 2023-03-19 12:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0024_delete_eventregistrationmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRegistrationModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when this entry was created in the system')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when the table data was last updated in the system')),
                ('is_paid', models.BooleanField(default=False)),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapps.eventmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event Registration Info',
                'verbose_name_plural': 'Event Registration Information',
                'db_table': 'event_registration_model',
            },
        ),
    ]
