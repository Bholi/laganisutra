from django.db import models

# Create your models here.

class PivotPoint(models.Model):
    script_name = models.CharField(max_length=100,null=True,blank=True)
    pivot_point = models.FloatField(null=True,blank=True)
    r1 = models.FloatField(null=True,blank=True)
    r2 = models.FloatField(null=True,blank=True)
    r3 = models.FloatField(null=True,blank=True)
    s1 = models.FloatField(null=True,blank=True)
    s2 = models.FloatField(null=True,blank=True)
    s3 = models.FloatField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)

    def __str__(self) -> str:
        return self.script_name
    
class FibonacciPivotPoint(models.Model):
    script_name = models.CharField(max_length=100,null=True,blank=True)
    pivot_point = models.FloatField(null=True,blank=True)
    r1 = models.FloatField(null=True,blank=True)
    r2 = models.FloatField(null=True,blank=True)
    r3 = models.FloatField(null=True,blank=True)
    s1 = models.FloatField(null=True,blank=True)
    s2 = models.FloatField(null=True,blank=True)
    s3 = models.FloatField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)


class CamrillaPivotPoint(models.Model):
    script_name = models.CharField(max_length=100,null=True,blank=True)
    pivot_point = models.FloatField(null=True,blank=True)
    r1 = models.FloatField(null=True,blank=True)
    r2 = models.FloatField(null=True,blank=True)
    r3 = models.FloatField(null=True,blank=True)
    r4 = models.FloatField(null=True,blank=True)
    s1 = models.FloatField(null=True,blank=True)
    s2 = models.FloatField(null=True,blank=True)
    s3 = models.FloatField(null=True,blank=True)
    s4 = models.FloatField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    time = models.TimeField(null=True,blank=True)
    