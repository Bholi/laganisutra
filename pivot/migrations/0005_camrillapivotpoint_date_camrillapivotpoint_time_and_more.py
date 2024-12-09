# Generated by Django 5.1.1 on 2024-09-23 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pivot', '0004_camrillapivotpoint'),
    ]

    operations = [
        migrations.AddField(
            model_name='camrillapivotpoint',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='camrillapivotpoint',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fibonaccipivotpoint',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='fibonaccipivotpoint',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pivotpoint',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='pivotpoint',
            name='time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]