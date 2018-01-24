# Generated by Django 2.0.1 on 2018-01-24 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('waiter', '0008_auto_20180124_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='cooking_instructions',
            field=models.CharField(default='notavaliable', max_length=500),
        ),
        migrations.AddField(
            model_name='order',
            name='customer_name',
            field=models.CharField(default='notavaliable', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='order_complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='order_contents',
            field=models.CharField(default='notavaliable', max_length=1000),
        ),
        migrations.AddField(
            model_name='order',
            name='purchase_method',
            field=models.CharField(default='notavaliable', max_length=100),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
