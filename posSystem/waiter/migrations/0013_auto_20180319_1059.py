# Generated by Django 2.0.2 on 2018-03-19 10:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('waiter', '0012_auto_20180319_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderextra',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2018, 3, 19, 10, 59, 36, 625139, tzinfo=utc)),
        ),
    ]
