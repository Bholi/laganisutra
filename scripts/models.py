from django.db import models

# Create your models here.
class AllScriptsData(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    ltp = models.FloatField(null=True,blank=True)
    percentChange = models.FloatField(null=True,blank=True)
    high = models.FloatField(null=True,blank=True)
    low = models.FloatField(null=True,blank=True)
    open = models.FloatField(null=True,blank=True)
    volume = models.FloatField(null=True,blank=True)
    turnover = models.FloatField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol