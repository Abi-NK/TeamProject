# Generated by Django 2.0.2 on 2018-03-01 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(max_length=1000)),
                ('course', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=100)),
                ('allergy', models.CharField(default='', max_length=1000)),
                ('calories', models.IntegerField(default=0)),
                ('image', models.CharField(default='na', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Seating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(default='Table 0', max_length=25)),
                ('available', models.BooleanField(default=True)),
                ('assistance', models.BooleanField(default=False)),
            ],
        ),
    ]
