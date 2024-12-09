"""
URL configuration for laganisutra project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('momentum.urls')),
    path('api/',include('scripts.urls')),
    path('api/livedata/',include('livedata.urls')),
    path('api/candles/',include('candlesticks.urls')),
    path('api/',include('ema.urls')),
    path('api/manupulation/',include('manupulation.urls')),
    path('api/',include('pivot.urls')),
    path('api/',include('sma.urls')),
    path('api/',include('sr.urls')),
    path('api/',include('stages.urls')),
    path('api/',include('subindices.urls')),
    path('api/summary/',include('summary.urls')),
    path('api/trending_stocks/',include('trending_stocks.urls')),
    path('api/floorsheet/',include('floorsheet.urls')),
]
