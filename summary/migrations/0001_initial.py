# Generated by Django 5.1.1 on 2024-09-26 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RsiSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('date', models.CharField(blank=True, max_length=100, null=True)),
                ('positive', models.IntegerField(blank=True, default=0, null=True)),
                ('negative', models.IntegerField(blank=True, default=0, null=True)),
                ('neutral', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
    ]