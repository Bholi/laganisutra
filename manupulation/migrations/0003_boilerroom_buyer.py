# Generated by Django 5.1.1 on 2024-10-23 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manupulation', '0002_boilerroom'),
    ]

    operations = [
        migrations.AddField(
            model_name='boilerroom',
            name='buyer',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
