# Generated by Django 4.1.7 on 2023-03-18 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapps', '0015_remove_eventmodel_fees'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventmodel',
            name='regular_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='eventmodel',
            name='sale_price',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]