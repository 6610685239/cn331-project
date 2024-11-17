from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from django.contrib.messages import get_messages
from accounts.views import *
from accounts.forms import *

class AccountsViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_password = "testpassword"
        self.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password=self.user_password
        )
        self.superuser = User.objects.create_superuser(
            username="admin331", email="admin@example.com", password="admin331"
        )

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_user_home_view(self):
        self.client.login(username="testuser", password=self.user_password)
        response = self.client.get(reverse("user_home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user_home.html")

    @patch("accounts.views.send_sendgrid_email")
    def test_register_view(self, mock_send_email):
        # ข้อมูลสำหรับการลงทะเบียน
        data = {
            "username": "6610000000",
            "password1": "StrongPassword123",  # รหัสผ่านต้องตรงกับข้อกำหนด
            "password2": "StrongPassword123",  # ยืนยันรหัสผ่านต้องตรงกัน
            "email": "testuser@dome.tu.ac.th"
        }
        # ส่ง request POST ไปยัง view
        response = self.client.post(reverse("register"), data)
        # ตรวจสอบว่าผู้ใช้ถูกสร้างในฐานข้อมูล
        self.assertTrue(User.objects.filter(username="testuser").exists())
        # ตรวจสอบว่า mock ฟังก์ชันการส่งอีเมลถูกเรียก
        mock_send_email.assert_called_once()



    @patch("accounts.views.send_sendgrid_email")
    def test_send_confirmation_email(self, mock_send_email):
        mock_send_email.return_value = None  # Mock SendGrid email
        self.client.post(
            reverse("register"),
            {
                "username": "6610000000",
                "email": "testuser@dome.tu.ac.th",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
            },
        )
        mock_send_email.assert_called_once()

    def test_login_view(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": self.user_password},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("user_home"))

    

    

    def test_confirm_email(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.get(reverse("confirm_email", args=[self.user.username]))
        self.assertEqual(response.status_code, 302)  # Redirects after confirming email
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)


class AboutViewTest(TestCase):
    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about.html")

class AboutNoLoginViewTest(TestCase):
    def test_about_no_login_view(self):
        response = self.client.get(reverse('about_no_login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "about_no_login.html")

class RegisterViewGetTest(TestCase):
    def test_register_view_get(self):
        # Send a GET request to the 'register' view
        response = self.client.get(reverse('register'))

        # Assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Assert that the correct template is rendered
        self.assertTemplateUsed(response, "register.html")

        # Assert that the form is in the context and is an instance of SignupForm
        self.assertIsInstance(response.context['form'], SignupForm)

class LoginViewTest(TestCase):
    def setUp(self):
        # สร้างผู้ใช้ตัวอย่าง
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin_user = User.objects.create_superuser(username="admin331", password="admin331")
    
    def test_login_successful(self):
        # ทดสอบการเข้าสู่ระบบที่ถูกต้อง
        response = self.client.post(reverse("home"), {
            "username": "testuser",
            "password": "testpass",
        })
        self.assertRedirects(response, reverse("user_home"))
        self.assertIn('_auth_user_id', self.client.session)

 

    def test_login_admin_redirect(self):
        # ทดสอบการเข้าสู่ระบบสำหรับผู้ใช้ admin
        response = self.client.post(reverse("home"), {
            "username": "admin331",
            "password": "admin331",
        })
        self.assertRedirects(response, "/admin/")

    def test_login_invalid_credentials(self):
        # ทดสอบการเข้าสู่ระบบที่ไม่ถูกต้อง
        response = self.client.post(reverse("home"), {
            "username": "invaliduser",
            "password": "invalidpass",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please enter a correct username and password. Note that both fields may be case-sensitive.")
