from django.db import models

# Create your models here.

class SubIndices(models.Model):
    indices = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(null=True,blank=True)
    current = models.CharField(max_length=100,null=True,blank=True)
    change = models.FloatField(null=True,blank=True)
    percent_change = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.indices