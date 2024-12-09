from django.db import models

# Create your models here.

class Sma5Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    sma_5_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class Sma10Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    sma_10_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class Sma20Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    sma_20_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self) -> str:
        return self.symbol
    
class Sma30Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    sma_30_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self) -> str:
        return self.symbol
    
class Sma50Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    sma_50_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol

class Sma100Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    sma_100_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self) -> str:
        return self.symbol
    
class Sma200Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    sma_200_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self) -> str:
        return self.symbol