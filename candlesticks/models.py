from django.db import models

# Create your models here.
class CandlestickPattern(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    candlestick_pattern = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
