# Generated by Django 5.1.3 on 2024-12-04 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LiveFeedData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(blank=True, null=True)),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('ltp', models.CharField(blank=True, max_length=100, null=True)),
                ('ltv', models.CharField(blank=True, max_length=100, null=True)),
                ('point_change', models.CharField(blank=True, max_length=100, null=True)),
                ('percent_change', models.CharField(blank=True, max_length=100, null=True)),
                ('open', models.CharField(blank=True, max_length=100, null=True)),
                ('high', models.CharField(blank=True, max_length=100, null=True)),
                ('low', models.CharField(blank=True, max_length=100, null=True)),
                ('volume', models.CharField(blank=True, max_length=100, null=True)),
                ('previous_closing', models.CharField(blank=True, max_length=100, null=True)),
                ('sent', models.BooleanField(blank=True, default=False, null=True)),
            ],
        ),
    ]
