
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import RsiModel,MacdModel,CciData,AwesomeOscillator,MomentumIndicator,StochasticRSI,WilliamPercentR,UltimateOscillator,BopModel,VwmaModel,AdxModel,ApoModel,BiasModel,BrarModel,CfoModel,CgModel,CmoModel,CoppockModel,CtiModel,DmModel,ErModel,EriModel,FisherModel,InertiaModel,KDJModel,KSTModel,PGOModel,PPOModel,PSLModel,PVOModel,QqeModel,ROCModel,RSXModel,RVGIModel,STCModel,SlopeModel,SMIErgodicModel,SqueezeModel,SqueezeProModel,StochasticOscillatorModel,TrixModel,TsiModel
from .serializers import RsiModelSerializer,MacdModelSerializer,CciModelSerializer,AwesomeOscillatorSerializer,MomentumIndicatorSerializer,StochasticRSISerializer,WilliamsPercentRSerializer,UltimateOscillatorSerializer,BopModelSerializer,VwmaModelSerializer,AdxModelSerializer,ApoModelSerializer,BiasModelSerializer,BrarModelSerializer,CfoModelSerializer,CgModelSerializer,CmoModelSerializer,CoppockModelSerializer,CtiModelSerializer,DmModelSerializer,ErModelSerializer,EriModelSerializer,FisherModelSerializer,InertiaModelSerializer,KdjModelSerializer,KstModelSerializer,PgoModelSerializer,PpoModelSerializer,PslModelSerializer,PvoModelSerializer,QqeModelSerializer,RocModelSerializer,RsxModelSerializer,RvgiModelSerializer,StcModelSerializer,SlopeModelSerializer,SmiModelSerializer,SqueezeModelSerializer,SqueezeProModelSerializer,StochModelSerializer,TrixModelSerializer,TsiModelSerializer
from rest_framework import status
from django.db.models import Max
# Create your views here.
@api_view(['GET'])
def rsi_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = RsiModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = RsiModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def macd_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = MacdModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = MacdModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def cci_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = CciData.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = CciModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def ao_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = AwesomeOscillator.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = AwesomeOscillatorSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def momentum_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = MomentumIndicator.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = MomentumIndicatorSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def stochrsi_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = StochasticRSI.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = StochasticRSISerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def willr_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = WilliamPercentR.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = WilliamsPercentRSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def uo_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = UltimateOscillator.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = UltimateOscillatorSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def bop_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = BopModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = BopModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def vwma_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = VwmaModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = VwmaModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['GET'])
def adx_view(request):
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = AdxModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = AdxModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)
    


@api_view(['GET'])
def get_apo_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = ApoModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = ApoModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_bias_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = BiasModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = BiasModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_brar_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = BrarModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = BrarModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_cfo_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = CfoModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = CfoModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_cg_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = CgModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = CgModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_cmo_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = CmoModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = CmoModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_coppock_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = CoppockModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = CoppockModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_cti_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = CtiModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = CtiModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_dm_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = DmModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = DmModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_er_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = ErModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = ErModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_eri_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = EriModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = EriModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_fisher_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = FisherModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = FisherModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_inertia_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = InertiaModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = InertiaModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_kdj_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = KDJModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = KdjModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_kst_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = KSTModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = KstModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_pgo_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = PGOModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = PgoModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_ppo_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = PPOModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = PpoModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_psl_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = PSLModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = PslModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_pvo_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = PVOModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = PvoModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_qqe_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = QqeModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = QqeModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_roc_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = ROCModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = RocModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_rsx_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = RSXModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = RsxModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_rvgi_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = RVGIModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = RvgiModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_stc_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = STCModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = StcModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_slope_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = SlopeModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = SlopeModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_smi_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = SMIErgodicModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = SmiModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_squeez_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = SqueezeModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = SqueezeModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_squeez_pro_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = SqueezeProModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = SqueezeProModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_stoch_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = StochasticOscillatorModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = StochModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_trix_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = TrixModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)
    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = TrixModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_tsi_data(request):
    # Filter the queryset based on symbol and date if provided in the query parameters
    symbol = request.GET.get('symbol', None)
    date = request.GET.get('date', None)

    # Initialize the queryset
    queryset = TsiModel.objects.all()

    # Apply filtering based on provided parameters
    if symbol:
        queryset = queryset.filter(symbol=symbol)
    if date:
        queryset = queryset.filter(date=date)

    latest_time = queryset.aggregate(Max('time'))['time__max']

    # Filter the queryset to get the data with the latest time
    latest_data = queryset.filter(time=latest_time)
    # Serialize the data
    serializer = TsiModelSerializer(latest_data, many=True)
    
    # Return the filtered data as a JSON response
    return Response(serializer.data, status=status.HTTP_200_OK)
