from django.urls import path
from ai.views import *
from . import views
urlpatterns = [
  


    path('electrician', ElectricianView.as_view(), name='electrician'),
    path('electrician/<int:pk>', ElectricianView.as_view(), name='electrician'),
    
    path('site', SitesView.as_view(), name='site'),
    path('site/<int:pk>', SitesView.as_view(), name='site'),



]
