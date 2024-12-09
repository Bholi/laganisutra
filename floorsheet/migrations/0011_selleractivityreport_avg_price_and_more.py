# Generated by Django 5.1.1 on 2024-12-01 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floorsheet', '0010_buyeractivityreport_avg_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='selleractivityreport',
            name='avg_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='selleractivityreport',
            name='max_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='selleractivityreport',
            name='min_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]