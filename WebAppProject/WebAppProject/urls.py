from django.contrib import admin
from django.urls import path, include
from accounts import views as accounts_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),  # รวม URLs ของ accounts
    path("", accounts_views.login_views, name="home"),
    path("", include("django.contrib.auth.urls")),  # รวม URL ของ Django auth
]
