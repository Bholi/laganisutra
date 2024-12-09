from rest_framework import serializers
from . import models

class RsiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RsiModel
        fields = '__all__'
        

class MacdModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MacdModel
        fields = '__all__'
        
class CciModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CciData
        fields = '__all__'

class AwesomeOscillatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AwesomeOscillator
        fields = '__all__'
        
        
class MomentumIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MomentumIndicator
        fields = '__all__'
        
class StochasticRSISerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StochasticRSI
        fields = '__all__'
        
class WilliamsPercentRSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WilliamPercentR
        fields = '__all__'
        
class UltimateOscillatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UltimateOscillator
        fields = '__all__'
        
class BopModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BopModel
        fields = '__all__'
        
class VwmaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.VwmaModel
        fields = '__all__'
        
class AdxModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AdxModel
        fields = '__all__'

class ApoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApoModel
        fields = '__all__'
        
class BiasModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BiasModel
        fields = '__all__'
        
class BrarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BrarModel
        fields = '__all__'
      
class CfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CfoModel
        fields = '__all__'
        
class CgModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CgModel
        fields = '__all__'

class CmoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CmoModel
        fields = '__all__'
        
class CoppockModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoppockModel
        fields = '__all__'       

class CtiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CtiModel
        fields = '__all__'   

class DmModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DmModel
        fields = '__all__'

class ErModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ErModel
        fields = '__all__'
        
class EriModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EriModel
        fields = '__all__'

class FisherModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FisherModel
        fields = '__all__'
        
class InertiaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InertiaModel
        fields = '__all__'

class KdjModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KDJModel
        fields = '__all__'
        
class KstModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.KSTModel
        fields = '__all__'

class PgoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PGOModel
        fields = '__all__'
        
class PpoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PPOModel
        fields = '__all__'       
        
class PslModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PSLModel
        fields = '__all__'         

class PvoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PVOModel
        fields = '__all__'  

class QqeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QqeModel
        fields = '__all__'  

class RocModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ROCModel
        fields = '__all__'  

class RsxModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RSXModel
        fields = '__all__'  

class RvgiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RVGIModel
        fields = '__all__' 
        
class StcModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.STCModel
        fields = '__all__' 
        
class SlopeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SlopeModel
        fields = '__all__'         
        
class SmiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SMIErgodicModel
        fields = '__all__'        

class SqueezeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SqueezeModel
        fields = '__all__' 
  
class SqueezeProModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SqueezeProModel
        fields = '__all__'       
        
class StochModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StochasticOscillatorModel
        fields = '__all__'          
        
class TrixModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TrixModel
        fields = '__all__' 
      
class TsiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TsiModel
        fields = '__all__' 
 
 
 
 
 
 
 
 
 