from django.db import models

class RsiSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f"{self.symbol} - Date: {self.date} - Positive: {self.positive}, Negative: {self.negative}, Neutral: {self.neutral}"

class MacdSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class AdxSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol

class CciSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class StochRsiSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class WillRSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class MomentumSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class AoSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class UoSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    

class VwmaSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class BopSummary(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    positive = models.IntegerField(default=0,null=True,blank=True)
    negative = models.IntegerField(default=0,null=True,blank=True)
    neutral = models.IntegerField(default=0,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol