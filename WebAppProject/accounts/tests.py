from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch
from django.contrib.messages import get_messages

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

    def test_home_view(self):
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

        # ตรวจสอบ status code
        self.assertEqual(response.status_code, 302)  # ต้องเป็น redirect
        self.assertRedirects(response, reverse("home"))

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

    def test_admin_login_redirect(self):
        response = self.client.post(
            reverse("login"),
            {"username": self.superuser.username, "password": "admin331"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/admin/")

    def test_user_logout(self):
        self.client.login(username="testuser", password=self.user_password)
        response = self.client.get(reverse("user_logout"))
        self.assertEqual(response.status_code, 302)

    def test_confirm_email(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.get(reverse("confirm_email", args=[self.user.username]))
        self.assertEqual(response.status_code, 302)  # Redirects after confirming email
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
