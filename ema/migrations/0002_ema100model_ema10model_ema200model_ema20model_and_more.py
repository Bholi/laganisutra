# Generated by Django 5.1.1 on 2024-09-19 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ema', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ema100Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('ema_100_value', models.FloatField(blank=True, null=True)),
                ('signal', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ema10Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('ema_10_value', models.FloatField(blank=True, null=True)),
                ('signal', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ema200Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('ema_200_value', models.FloatField(blank=True, null=True)),
                ('signal', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ema20Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('ema_20_value', models.FloatField(blank=True, null=True)),
                ('signal', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ema30Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('ema_30_value', models.FloatField(blank=True, null=True)),
                ('signal', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ema50Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('ema_50_value', models.FloatField(blank=True, null=True)),
                ('signal', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
    ]