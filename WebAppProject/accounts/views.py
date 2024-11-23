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
from tu_party.models import Party
from django.utils.timezone import now


def home(request):
    return render(request, "home.html")


def user_home(request):
    posts = Post.objects.prefetch_related(
        Prefetch("comments", queryset=Comment.objects.order_by("-created_at"))
    ).order_by("-created_at")
    parties = Party.objects.prefetch_related("interested_users").order_by("event_date")
    return render(request, "user_home.html", {"posts": posts, "parties": parties})


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
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            remember_me = form.cleaned_data.get(
                "remember"
            )  # Get the 'remember me' checkbox value
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if remember_me:  # If remember me is checked
                    request.session.set_expiry(
                        60 * 60 * 24 * 30
                    )  # Set session to last for 30 days
                else:
                    request.session.set_expiry(
                        0
                    )  # Session expires when the browser is closed
                if user.is_superuser:
                    return redirect("/admin/")
                else:
                    return redirect("user_home")
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "home.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user until email is verified
            user.save()
            send_confirmation_email(user)  # Send the confirmation email
            messages.success(request, "Please verify your email.")
            return render(request, "register.html", {"form": form, "show_modal": True})
    else:
        form = SignupForm()

    return render(request, "register.html", {"form": form, "show_modal": False})


def send_confirmation_email(user):
    confirmation_url = (
        f"{settings.DOMAIN}{reverse('confirm_email', args=[user.username])}"
    )
    subject = "ยืนยันการสมัครสมาชิก"
    message = f"""
    สวัสดี {user.username},

    ขอบคุณที่สมัครใช้งาน TUTalk! 
    โปรดยืนยันที่อยู่อีเมลของคุณโดยคลิกลิงก์ด้านล่าง:

    {confirmation_url}

    หากคุณไม่ได้สมัครใช้งาน TUTalk กรุณาเพิกเฉยต่ออีเมลฉบับนี้

    ขอบคุณ,
    ทีมงาน TUTalk
    """

    # Send confirmation email using SendGrid
    send_sendgrid_email(user.email, subject, message)


def confirm_email(request, username):
    user = get_object_or_404(User, username=username)
    user.is_active = True  # เปิดใช้งานบัญชีผู้ใช้
    user.save()
    login(request, user)  # ล็อกอินอัตโนมัติหลังยืนยัน
    messages.success(request, "Verify Email Success! You have logged in")
    return redirect("home")


def about(request):
    return render(request, "about.html")


def about_no_login(request):
    return render(request, "about_no_login.html")
