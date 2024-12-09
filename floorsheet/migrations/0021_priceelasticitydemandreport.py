# Generated by Django 5.1.1 on 2024-12-01 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floorsheet', '0020_alter_pricevolatilityvolumereport_price_change_percentage_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceElasticityDemandReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('price_change_percentage', models.FloatField(blank=True, null=True)),
                ('quantity_change_percentage', models.FloatField(blank=True, null=True)),
                ('ped', models.FloatField(blank=True, null=True)),
                ('market_condition', models.CharField(blank=True, max_length=255, null=True)),
                ('interpretation', models.TextField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]
