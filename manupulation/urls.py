from django.urls import path
from .views import TradeAnalysisList,floorsheet_data_list,embezzlement_data_list,layering_spoofing_data_list,ponzi_scheme_data_list,ramping_data_list,threshold_tuning_data_list,wash_trade_list

urlpatterns = [
    path('trade-analysis/', TradeAnalysisList.as_view(), name='trade-analysis-list'),
    path('boiler-room/', floorsheet_data_list, name='floorsheet_data_list'),
    path('embezzlement/',embezzlement_data_list),
    path('layering/',layering_spoofing_data_list),
    path('ponzi/',ponzi_scheme_data_list),
    path('ramping/',ramping_data_list),
    path('threshold/',threshold_tuning_data_list),
    path('washing/',wash_trade_list),
]   