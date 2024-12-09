from django.urls import path
from . import views
urlpatterns =[
    path('ema5/',views.ema5_view,name='ema5'),
    path('ema10/',views.ema10_view,name='ema10'),
    path('ema20/',views.ema20_view,name='ema20'),
    path('ema30/',views.ema30_view,name='ema30'),
    path('ema50/',views.ema50_view,name='ema50'),
    path('ema100/',views.ema100_view,name='ema100'),
    path('ema200/',views.ema200_view,name='ema200'),
]