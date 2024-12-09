from django.urls import path
from . import views

urlpatterns=[
    path('sma5/',views.sma5_view,name='sma5'),
    path('sma10/',views.sma10_view,name='sma10'),
    path('sma20/',views.sma20_view,name='sma20'),
    path('sma30/',views.sma30_view,name='sma30'),
    path('sma50/',views.sma50_view,name='sma50'),
    path('sma100/',views.sma100_view,name='sma100'),
    path('sma200/',views.sma200_view,name='sma200'),
]

