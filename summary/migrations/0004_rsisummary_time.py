# Generated by Django 5.1.1 on 2024-09-26 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('summary', '0003_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rsisummary',
            name='time',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]