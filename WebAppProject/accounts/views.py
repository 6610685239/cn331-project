from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .forms import SignupForm, LoginForm
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse


def home(request):
    return render(request, "home.html")


def user_home(request):
    return render(request, "user_home.html")


def login_views(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)  # Ensure you are using your LoginForm
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Check if user is superuser
                if user.is_superuser:
                    return redirect("/admin/")
                else:
                    return redirect("user_home")
    else:
        form = LoginForm()

    return render(request, "home.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # ส่ง email ยืนยัน
            send_confirmation_email(user)
            messages.success(request, "สมัครสมาชิกสำเร็จ! โปรดยืนยัน email ของคุณ")
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "register.html", {"form": form})


def send_confirmation_email(user):
    confirmation_url = (
        f"{settings.DOMAIN}{reverse('confirm_email', args=[user.username])}"
    )
    send_mail(
        "ยืนยันการสมัครสมาชิก",
        f"โปรดคลิกลิงก์ต่อไปนี้เพื่อยืนยันการสมัครสมาชิกเว็บ TU talk ไม่โกงแน่นอน: {confirmation_url}",
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def confirm_email(request, username):
    user = get_object_or_404(User, username=username)
    user.is_active = True  # เปิดใช้งานบัญชีผู้ใช้
    user.save()
    login(request, user)  # ล็อกอินอัตโนมัติหลังยืนยัน
    messages.success(request, "ยืนยัน email สำเร็จ! คุณได้เข้าสู่ระบบแล้ว")
    return redirect("home")


def user_logout(request):
    logout(request)
    return redirect("login")
