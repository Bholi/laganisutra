# Generated by Django 5.1.1 on 2024-10-21 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floorsheet', '0002_alter_floorsheetdata_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floorsheetdata',
            name='quantity',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='floorsheetdata',
            name='rate',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
