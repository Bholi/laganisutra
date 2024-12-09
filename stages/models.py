from django.db import models

# Create your models here.
class MarketCycleStage(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    stage = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(null=True,blank=True)