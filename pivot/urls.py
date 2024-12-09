from django.urls import path
from .views import pivot_point_view,fibonacci_pivot_point_view,camarilla_pivot_point
urlpatterns=[
    path('pivot/',pivot_point_view,name='pivot'),
    path('fibopivot/',fibonacci_pivot_point_view,name='fibopivot'),
    path('camrilla/',camarilla_pivot_point,name='camrilla'),
]