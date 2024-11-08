from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # รวม URLs ของ accounts
    path(
        "", auth_views.LoginView.as_view(template_name="home.html"), name="home"
    ),  # ใช้ home.html แทน login.html
    path("", include("django.contrib.auth.urls")),  # รวม URL ของ Django auth
]
