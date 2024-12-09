# Generated by Django 5.1.1 on 2024-11-29 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floorsheet', '0004_floorsheetdata_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockSummaryReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('total_quantity_traded', models.IntegerField(blank=True, null=True)),
                ('no_of_transactions', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]