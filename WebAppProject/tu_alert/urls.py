from django.urls import path
from . import views

app_name = "tu_alert"

urlpatterns = [
    path("", views.alert_list, name="alert_list"),
]
