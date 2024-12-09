from django.db import models

# Create your models here.
class SupportResistance(models.Model):
    datetime = models.DateTimeField(null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    pivot = models.FloatField(null=True,blank=True)
    resistance_1 = models.FloatField(null=True,blank=True)
    support_1 = models.FloatField(null=True,blank=True)
    resistance_2 = models.FloatField(null=True,blank=True)
    support_2 = models.FloatField(null=True,blank=True)

    class Meta:
        unique_together = ('datetime', 'symbol')
        verbose_name = "Support and Resistance"
        verbose_name_plural = "Support and Resistance"

    def __str__(self):
        return f"{self.symbol} - {self.datetime}"