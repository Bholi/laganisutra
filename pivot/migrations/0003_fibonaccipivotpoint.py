# Generated by Django 5.1.1 on 2024-09-20 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pivot', '0002_pivotpoint_r1_pivotpoint_r2_pivotpoint_r3_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FibonacciPivotPoint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_name', models.CharField(blank=True, max_length=100, null=True)),
                ('high', models.FloatField(blank=True, null=True)),
                ('low', models.FloatField(blank=True, null=True)),
                ('close', models.FloatField(blank=True, null=True)),
                ('pivot_point', models.FloatField(blank=True, null=True)),
                ('r1', models.FloatField(blank=True, null=True)),
                ('r2', models.FloatField(blank=True, null=True)),
                ('r3', models.FloatField(blank=True, null=True)),
                ('s1', models.FloatField(blank=True, null=True)),
                ('s2', models.FloatField(blank=True, null=True)),
                ('s3', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
