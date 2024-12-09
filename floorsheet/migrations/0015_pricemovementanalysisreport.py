# Generated by Django 5.1.1 on 2024-12-01 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('floorsheet', '0014_tradevolanalysisreport'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceMovementAnalysisReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(blank=True, max_length=100, null=True)),
                ('first_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('last_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('percent_change', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('trend', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]