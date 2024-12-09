# Generated by Django 5.1.1 on 2024-09-23 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ema', '0002_ema100model_ema10model_ema200model_ema20model_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ema100model',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema100model',
            name='time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema10model',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema10model',
            name='time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema200model',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema200model',
            name='time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema20model',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema20model',
            name='time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema30model',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema30model',
            name='time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema50model',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema50model',
            name='time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema5model',
            name='date',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='ema5model',
            name='time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
