# Generated by Django 4.1.7 on 2023-03-18 19:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0009_rename_address_eventmodel_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventmodel',
            name='working_since',
        ),
    ]
