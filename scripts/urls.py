from django.urls import path
from .views import alldata_view
urlpatterns=[
    path('scripts/',alldata_view,name='scripts'),
]