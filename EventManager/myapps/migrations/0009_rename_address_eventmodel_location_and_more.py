# Generated by Django 4.1.7 on 2023-03-18 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0008_rename_user_eventmodel_organization_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eventmodel',
            old_name='address',
            new_name='location',
        ),
        migrations.RemoveField(
            model_name='eventmodel',
            name='fees_currency',
        ),
        migrations.AlterField(
            model_name='eventmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]