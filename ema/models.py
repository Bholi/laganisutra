from django.db import models

# Create your models here.
class Ema5Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    ema_5_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)


    def __str__(self) -> str:
        return self.symbol
    
class Ema10Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    ema_10_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class Ema20Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    ema_20_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol

class Ema30Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    ema_30_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class Ema50Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    ema_50_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class Ema100Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    ema_100_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class Ema200Model(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    ema_200_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol