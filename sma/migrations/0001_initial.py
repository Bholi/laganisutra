# Generated by Django 5.1.1 on 2024-09-19 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sma5Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('close_price', models.FloatField(blank=True, null=True)),
                ('sma_5_value', models.FloatField(blank=True, null=True)),
                ('signal', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]