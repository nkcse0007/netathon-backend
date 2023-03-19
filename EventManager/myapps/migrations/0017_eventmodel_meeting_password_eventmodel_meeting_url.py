# Generated by Django 4.1.7 on 2023-03-18 23:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0016_alter_eventmodel_regular_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodel',
            name='meeting_password',
            field=models.URLField(default=datetime.datetime(2023, 3, 18, 23, 31, 19, 751343, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='eventmodel',
            name='meeting_url',
            field=models.URLField(default=datetime.datetime(2023, 3, 18, 23, 31, 30, 637099, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]