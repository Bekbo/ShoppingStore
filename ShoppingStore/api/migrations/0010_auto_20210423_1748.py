# Generated by Django 3.1 on 2021-04-23 11:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20210423_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 4, 23, 17, 48, 38, 984406)),
        ),
    ]
