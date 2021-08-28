from django.urls import path
from . import views

urlpatterns = [
    path('', views.open_seleted_channels, name='open_seleted_channels'),
]
