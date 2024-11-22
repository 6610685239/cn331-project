from django.urls import path
from . import views

app_name = "tu_party"

urlpatterns = [
    path("", views.party_list, name="party_list"),
    path("create/", views.create_party, name="create_party"),
    path("<int:party_id>/interest/", views.interest_party, name="interest_party"),
]
