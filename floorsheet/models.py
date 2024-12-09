from django.db import models

# Create your models here.
class Sector(models.Model):
    id = models.AutoField(primary_key=True)  # Auto-incrementing ID
    name = models.CharField(max_length=100, unique=True,null=True,blank= True)  # Name of the sector
    symbols = models.TextField(null=True, blank=True)  # Comma-separated symbols in the sector
    def __str__(self):
        return self.name

class FloorSheetData(models.Model):
    transaction_no = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.CharField(max_length=100,null=True,blank=True)
    rate = models.CharField(max_length=100,null=True,blank=True)
    amount = models.CharField(max_length=100,null=True,blank=True)
    date = models.DateField(null=True,blank=True)


    def __str__(self):
        return self.symbol
    
class StockSummaryReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    total_quantity_traded = models.IntegerField(null=True,blank=True)
    no_of_transactions = models.IntegerField(null=True,blank=True)
    total_value = models.FloatField(null=True, blank=True)  # New field
    average_rate = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True,blank=True)

class BuyerActivityReport(models.Model):
    buyer_id = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    total_quantity_bought = models.IntegerField(null=True,blank=True)
    total_amount_spent = models.FloatField(null=True,blank=True)
    min_price = models.FloatField(null=True, blank=True)
    max_price = models.FloatField(null=True, blank=True)
    avg_price = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True,blank=True)  # Add the date field

class SellerActivityReport(models.Model):
    seller_id = models.CharField(max_length=100,null=True,blank=True)
    symbol = models.CharField(max_length=100,null=True,blank=True)
    total_quantity_sold = models.FloatField(null=True,blank=True)
    total_amount_received = models.FloatField(null=True,blank=True)
    min_price = models.FloatField(null=True, blank=True)
    max_price = models.FloatField(null=True, blank=True)
    avg_price = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True,blank=True)


class HighValueTransactionReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buyer = models.CharField(max_length=100,null=True,blank=True)
    seller = models.CharField(max_length=100,null=True,blank=True)
    quantity = models.FloatField(null=True,blank=True)
    rate = models.FloatField(null=True,blank=True)
    amount = models.FloatField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)


class VolatilityAnalysisReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    min_rate = models.FloatField(null=True,blank=True)
    max_rate = models.FloatField(null=True,blank=True)
    avg_rate = models.FloatField(null=True,blank=True)
    stddev_rate = models.FloatField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)

class TradeVolAnalysisReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    total_quantity_traded = models.IntegerField(null=True, blank=True)
    no_of_transactions = models.IntegerField(null=True, blank=True)
    min_trade_vol = models.FloatField(null=True, blank=True)
    max_trade_vol = models.FloatField(null=True, blank=True)
    avg_trade_volume = models.FloatField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)


class PriceMovementAnalysisReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    first_rate = models.DecimalField(max_digits=20, decimal_places=2,null=True,blank=True)
    last_rate = models.DecimalField(max_digits=20, decimal_places=2,null=True,blank=True)
    percent_change = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    trend = models.CharField(max_length=50,null=True,blank=True)
    date = models.DateField(null=True,blank=True)


class LiquidityConcentrationReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    total_quantity_traded = models.IntegerField(null=True,blank=True)
    lcr_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    liquidity_concentration = models.CharField(max_length=100,null=True,blank=True)
    interpretation = models.TextField(null=True,blank=True)
    date=models.DateField(null=True,blank=True)

class PriceVolatilityVolumeReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    price_change_percentage = models.FloatField(null=True,blank=True)
    volume_change_percentage = models.FloatField(null=True,blank=True)
    vvr = models.FloatField(null=True,blank=True)
    market_condition = models.CharField(max_length=255,null=True,blank=True)
    interpretation = models.TextField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)


class PriceElasticityDemandReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    price_change_percentage = models.FloatField(null=True,blank=True)
    quantity_change_percentage = models.FloatField(null=True,blank=True)
    ped = models.FloatField(null=True,blank=True)
    market_condition = models.CharField(max_length=255,null=True,blank=True)
    interpretation = models.TextField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)

class StockPriceRangeReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    highest_price = models.FloatField(null=True,blank=True)
    lowest_price = models.FloatField(null=True,blank=True)
    price_range = models.FloatField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)

class BrokerVolumeConcentrationReport(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    buying_brokers = models.IntegerField(null=True,blank=True)
    selling_brokers = models.IntegerField(null=True,blank=True)
    share_quantity = models.FloatField(null=True,blank=True)
    num_transactions = models.IntegerField(null=True,blank=True)
    date = models.DateField(null=True,blank=True)

