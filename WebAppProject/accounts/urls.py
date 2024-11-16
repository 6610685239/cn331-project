# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("confirm-email/<str:username>/", views.confirm_email, name="confirm_email"),
    path("user-home/", views.user_home, name="user_home"),
    path("about/", views.about, name="about"),
    path("about-no-login/", views.about_no_login, name="about_no_login"),
]
