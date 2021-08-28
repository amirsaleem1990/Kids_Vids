from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_selected_channels, name='show_selected_channels'),
]
