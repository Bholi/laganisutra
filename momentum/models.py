from django.db import models

# Create your models here.

class RsiModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    rsi_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,blank=True,null=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.symbol} - RSI: {self.rsi_value}"

class MacdModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    macd_line = models.FloatField(null=True,blank=True)
    signal_line = models.FloatField(null=True,blank=True)
    macd_histogram = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    

class CciData(models.Model):
    script_name = models.CharField(max_length=100,null=True,blank=True)
    high = models.FloatField(null=True,blank=True)
    low = models.FloatField(null=True,blank=True)
    close = models.FloatField(null=True,blank=True)
    cci = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.script_name
    

class AwesomeOscillator(models.Model):
    script_name = models.CharField(max_length=100,null=True,blank=True)
    high = models.FloatField(null=True,blank=True)
    low = models.FloatField(null=True,blank=True)
    ao_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.script_name
    
class MomentumIndicator(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    close_price = models.FloatField(null=True,blank=True)
    mom_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class StochasticRSI(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    close_price = models.FloatField(null=True,blank=True)
    stochrsi_k = models.FloatField(null=True,blank=True)
    stochrsi_d = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,blank=True,null=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class WilliamPercentR(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    willr_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class UltimateOscillator(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    uo_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class BopModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    bop = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,blank=True,null=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self) -> str:
        return self.symbol
    
class VwmaModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    vwma_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self) -> str:
        return self.symbol
    
class AdxModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    adx_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,blank=True,null=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    
    def __str__(self) -> str:
        return self.symbol
    

class ApoModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    apo_value = models.CharField(max_length=100,null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.symbol

class BiasModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    bias_value = models.CharField(max_length=100,null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.symbol
    
class BrarModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    br_value = models.FloatField(null=True,blank=True)
    ar_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class CfoModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    cfo_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
class CgModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    cg_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class CmoModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    cmo_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class CoppockModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    coppock_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    

class CtiModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    cti_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class DmModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    plus_dm = models.FloatField(null=True,blank=True)
    minus_dm = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class ErModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    efficiency_ratio = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class EriModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    bull_power = models.FloatField(null=True,blank=True)
    bear_power = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class FisherModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    fisher_transform = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class InertiaModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    inertia = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol

class KDJModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    k_value = models.FloatField(null=True,blank=True)
    d_value = models.FloatField(null=True,blank=True)
    j_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class KSTModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    kst_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class PGOModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    pgo_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class PPOModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    ppo_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class PSLModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    psl_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol

class PVOModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    pvo_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol

class QqeModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    fast_qqe = models.FloatField(null=True,blank=True)
    slow_qqe = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    
class ROCModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    roc = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class RSXModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    rsx = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100, null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class RVGIModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    rvgi = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class STCModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    stc = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class SlopeModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    slope = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class SMIErgodicModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    smi_ergodic = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol

class SqueezeModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    squeeze_indicator = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol

class SqueezeProModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    squeeze_pro = models.CharField(max_length=100,null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol
    
class StochasticOscillatorModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    k = models.FloatField(null=True,blank=True)
    d = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)  # To store Buy, Sell, or Neutral
    def __str__(self):
        return self.symbol
    
class TDSequentialModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    td_Setup = models.IntegerField(null=True,blank=True)
    td_Countdown = models.IntegerField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)  # e.g., 'Signal', 'No Signal'
    def __str__(self):
        return self.symbol
    
class TrixModel(models.Model):
    symbol = models.CharField(max_length=100,null=True,blank=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    trix_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol

class TsiModel(models.Model):
    symbol = models.CharField(max_length=100,blank=True,null=True)
    date = models.CharField(max_length=100,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    tsi_value = models.FloatField(null=True,blank=True)
    signal = models.CharField(max_length=100,null=True,blank=True)
    def __str__(self):
        return self.symbol 
  







