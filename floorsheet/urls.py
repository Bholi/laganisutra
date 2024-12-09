from django.urls import path
from .views import FloorSheetDataView,get_stock_summary_report_data,get_buyer_activity_report,get_seller_activity_report,delete_all_buyer_activity_reports,delete_all_seller_activity_reports,get_high_value_transaction_report,get_volatility_analysis_report,get_trade_vol_analysis_report,delete_all_tradevol_activity_reports,get_price_movement_analysis_report,get_lcr_analysis_report,get_pvvr_analysis_report,get_price_elasticity_analysis_report,get_stock_price_range_report,get_broker_volume_report,sectors_view,receive_floorsheet_data
urlpatterns = [
    path('', FloorSheetDataView.as_view(), name='floorsheet_data'),
    path('sync/', receive_floorsheet_data, name='receive_floorsheet_data'),
    path('stock_summary_report/',get_stock_summary_report_data),
    path('buyer_activity_report/',get_buyer_activity_report),
    path('buyer_activity_report/delete/',delete_all_buyer_activity_reports),
    path('seller_activity_report/',get_seller_activity_report),
    path('seller_activity_report/delete/',delete_all_seller_activity_reports),
    path('high_value_transaction_report/',get_high_value_transaction_report),
    path('volatility_analysis_report/',get_volatility_analysis_report),
    path('trade_vol_analysis_report/',get_trade_vol_analysis_report),
    path('trade_vol_analysis_report/delete/',delete_all_tradevol_activity_reports),
    path('price_movement_analysis_report/',get_price_movement_analysis_report),
    path('lcr_report/',get_lcr_analysis_report),
    path('pvvr_report/',get_pvvr_analysis_report),
    path('price_elasticity/',get_price_elasticity_analysis_report),
    path('stock_price_range/',get_stock_price_range_report),
    path('broker_volume_report/',get_broker_volume_report),
    path('sectors/',sectors_view),
]