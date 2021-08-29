from django.urls import path
from . import views



urlpatterns = [
    path('', views.select_channels, name='select_channels'),
]
