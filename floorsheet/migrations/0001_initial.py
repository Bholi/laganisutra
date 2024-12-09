# Generated by Django 5.1.1 on 2024-10-21 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FloorSheetData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_no', models.CharField(blank=True, max_length=100, null=True)),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('buyer', models.CharField(blank=True, max_length=100, null=True)),
                ('seller', models.CharField(blank=True, max_length=100, null=True)),
                ('quantity', models.FloatField(blank=True, null=True)),
                ('rate', models.FloatField(blank=True, null=True)),
                ('amount', models.FloatField(blank=True, null=True)),
            ],
        ),
    ]
