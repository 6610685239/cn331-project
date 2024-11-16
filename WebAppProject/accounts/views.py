from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from .forms import SignupForm, LoginForm
from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from tu_talk.models import Post, Comment
from django.db.models import Prefetch


def home(request):
    return render(request, "home.html")


def user_home(request):
    posts = Post.objects.prefetch_related(
        Prefetch("comments", queryset=Comment.objects.order_by("-created_at"))
    ).order_by("-created_at")
    return render(request, "user_home.html", {"posts": posts})


def send_sendgrid_email(to_email, subject, text_content):
    # Set up SendGrid API client
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    # Create the email message
    from_email = Email("tutalkofficial@gmail.com")
    to_email = To(to_email)
    content = Content("text/plain", text_content)

    # Create the email and send it
    mail = Mail(from_email, to_email, subject, content)

    # Send the email
    response = sg.send(mail)

    # Print the response for debugging
    print(f"SendGrid Response: {response.status_code}, {response.body}")
    return response


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
    subject = "ยืนยันการสมัครสมาชิก"
    message = (
        f"โปรดคลิกลิงก์ต่อไปนี้เพื่อยืนยันการสมัครสมาชิกเว็บ TU talk ไม่โกงแน่นอน: {confirmation_url}"
    )

    # Send confirmation email using SendGrid
    send_sendgrid_email(user.email, subject, message)


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


def about(request):
    return render(request, "about.html")
