from django.urls import path
from . import views
urlpatterns=[
    path('rsi/',views.get_rsi_summary),
    path('macd/',views.get_macd_summary),
    path('adx/',views.get_adx_summary),
    path('cci/',views.get_cci_summary),
    path('ao/',views.get_ao_summary),
    path('stoch/',views.get_stoch_summary),
    path('willr/',views.get_willr_summary),
    path('mom/',views.get_mom_summary),
    path('uo/',views.get_uo_summary),
    path('bop/',views.get_bop_summary),
    path('vwma/',views.get_vwma_summary),
]