# Generated by Django 5.1.1 on 2024-12-01 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floorsheet', '0023_rename_stock_symbol_stockpricerangereport_symbol'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrokerVolumeConcentrationReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('buying_brokers', models.IntegerField(blank=True, null=True)),
                ('selling_brokers', models.IntegerField(blank=True, null=True)),
                ('share_quantity', models.FloatField(blank=True, null=True)),
                ('num_transactions', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
