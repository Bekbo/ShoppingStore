# Generated by Django 3.1 on 2021-05-13 12:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_auto_20210513_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_created',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 13, 18, 39, 24, 981312)),
        ),
    ]
