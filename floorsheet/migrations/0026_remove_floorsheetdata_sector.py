# Generated by Django 5.1.3 on 2024-12-04 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('floorsheet', '0025_sector_floorsheetdata_sector'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='floorsheetdata',
            name='sector',
        ),
    ]
