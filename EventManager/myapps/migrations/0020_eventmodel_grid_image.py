# Generated by Django 4.1.7 on 2023-03-19 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0019_alter_eventmodel_meeting_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventmodel',
            name='grid_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]