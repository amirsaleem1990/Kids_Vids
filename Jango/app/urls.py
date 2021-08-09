from django.conf.urls import url
from . import views
app_name = "app"

urlpatterns = [
    url("", views.dashboard, name="dashboard"),
]