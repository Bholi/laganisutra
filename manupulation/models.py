from django.db import models

# Create your models here.

class TradeAnalysis(models.Model):
    transact_no = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    repeated_trades_flag = models.BooleanField(default=False,null=True,blank=True)
    price_manipulation_flag = models.BooleanField(default=False,null=True,blank=True)
    painting_the_tape_flag = models.BooleanField(default=False,null=True,blank=True)
    volume_spike_flag = models.BooleanField(default=False,null=True,blank=True)
    circular_trading_flag = models.BooleanField(default=False,null=True,blank=True)
    pump_flag = models.BooleanField(default=False,null=True,blank=True)
    dump_flag = models.BooleanField(default=False,null=True,blank=True)
    seller_reappears_flag = models.BooleanField(default=False,null=True,blank=True)
    suspicious = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.symbol
    

class BoilerRoom(models.Model):
    transaction_no = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    volume = models.CharField(max_length=100,null=True,blank=True)
    boiler_room_flag = models.BooleanField(default=False,null=True,blank=True)

class EmbezzlementData(models.Model):
    transaction_no = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    volume = models.CharField(max_length=100,null=True,blank=True)
    embezzlement_flag = models.BooleanField(default=False,null=True,blank=True)


class LayeringSpoofingData(models.Model):
    transaction_no = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    volume = models.CharField(max_length=100,null=True,blank=True)
    layering_flag = models.BooleanField(default=False,null=True,blank=True)
    spoofing_flag = models.BooleanField(default=False,null=True,blank=True)

class PonziSchemeData(models.Model):
    transaction_no = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    volume = models.CharField(max_length=100,null=True,blank=True)
    ponzi_flag = models.BooleanField(default=False,null=True,blank=True)

class RampingData(models.Model):
    transaction_no = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    volume = models.CharField(max_length=100,null=True,blank=True)
    ramping_flag = models.CharField(max_length=100,null=True,blank=True)


class ThresholdTuningData(models.Model):
    transaction_no = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    volume = models.CharField(max_length=100,null=True,blank=True)
    high_value_flag = models.BooleanField(default=False,null=True,blank=True)
    low_value_flag = models.BooleanField(default=False,null=True,blank=True)
    frequent_buyer_flag = models.BooleanField(default=False,null=True,blank=True)
    rare_buyer_flag = models.BooleanField(default=False,null=True,blank=True)
    potential_anomaly = models.BooleanField(default=False,null=True,blank=True)



class WashTradeData(models.Model):
    transaction_no = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    price = models.FloatField(null=True,blank=True)
    volume = models.CharField(max_length=100,blank=True,null=True)
    wash_trade_flag = models.BooleanField(default=False,null=True,blank=True)