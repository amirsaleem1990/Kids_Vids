from django.urls import path
from . import views

urlpatterns = [
    path('', views.auth_, name='auth_'),
    path('auth_check', views.auth_check, name='auth_check'),
]
