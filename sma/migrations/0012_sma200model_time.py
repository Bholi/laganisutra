# Generated by Django 5.1.1 on 2024-09-23 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sma', '0011_sma100model_date_sma100model_time_sma10model_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sma200model',
            name='time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
