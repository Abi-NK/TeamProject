# Generated by Django 2.0.2 on 2018-03-14 21:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('waiter', '0008_auto_20180309_0841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderextra',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 14, 21, 38, 13, 211701, tzinfo=utc)),
        ),
    ]
