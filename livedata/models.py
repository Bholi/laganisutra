from django.db import models

# Create your models here.

class LiveFeedData(models.Model):
    datetime = models.DateTimeField(null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    ltp = models.CharField(max_length=100,null=True,blank=True)
    ltv = models.CharField(max_length=100,null=True,blank=True)
    point_change = models.CharField(max_length=100,null=True,blank=True)
    percent_change = models.CharField(max_length=100,null=True,blank=True)
    open = models.CharField(max_length=100,null=True,blank=True)
    high = models.CharField(max_length=100,null=True,blank=True)
    low = models.CharField(max_length=100,null=True,blank=True)
    volume = models.CharField(max_length=100,null=True,blank=True)
    previous_closing = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self):
        return self.symbol