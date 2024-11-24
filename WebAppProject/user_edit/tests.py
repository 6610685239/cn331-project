from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile
from .forms import UserEditForm, ProfileEditForm


class ProfileViewTests(TestCase):
    def setUp(self):
        # Create a test user and profile
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.profile, created = Profile.objects.get_or_create(user=self.user)
        
        # Create a superuser
        self.admin_user = User.objects.create_superuser(username='adminuser', password='adminpass')

    def test_profile_view_authenticated_user(self):
        # Login as a regular user
        self.client.login(username='testuser', password='testpass')
        
        # Access the profile view
        response = self.client.get(reverse('user_edit:profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_edit/profile.html')
        self.assertContains(response, self.user.username)

    def test_profile_view_redirect_unauthenticated_user(self):
        # Access the profile view without logging in
        response = self.client.get(reverse('user_edit:profile'))
        
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertTrue(response.url.startswith(reverse('home')))

    def test_profile_edit_view_authenticated_user(self):
        # Login as a regular user
        self.client.login(username='testuser', password='testpass')
        
        # Access the profile_edit view
        response = self.client.get(reverse('user_edit:profile_edit'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_edit/profile_edit.html')

    def test_profile_edit_post_valid_data(self):
        # Login as a regular user
        self.client.login(username='testuser', password='testpass')
        
        # Send POST request with valid data
        data = {
            'username': 'newusername',
            'bio': 'Updated bio',
            'faculty': 'Engineering',
        }
        response = self.client.post(reverse('user_edit:profile_edit'), data)
        
        self.assertRedirects(response, reverse('user_edit:profile'))
        self.user.refresh_from_db()
        self.profile.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.profile.bio, 'Updated bio')
        self.assertEqual(self.profile.faculty, 'Engineering')

    def test_profile_edit_view_redirect_admin_user(self):
        # Login as an admin user
        self.client.login(username='adminuser', password='adminpass')
        
        # Access the profile_edit view
        response = self.client.get(reverse('user_edit:profile_edit'))
        
        self.assertRedirects(response, reverse('admin:index'))

class ProfileEditView_ifnothave_Tests(TestCase):
    def setUp(self):
        # สร้างผู้ใช้และล็อกอิน
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')

        # ลบ Profile ออกจากผู้ใช้
        self.user.profile.delete()

    def test_create_profile_if_not_exists(self):
        # เข้าถึง view profile_edit ซึ่งต้องสร้าง profile ใหม่
        response = self.client.get(reverse('user_edit:profile_edit'))

        # ตรวจสอบว่า profile ถูกสร้างขึ้นใหม่
        self.assertEqual(Profile.objects.filter(user=self.user).count(), 1)
        self.assertEqual(response.status_code, 200)



class ProfileModelTests(TestCase):


    def setUp(self):
        # สร้าง User โดย Signal จะสร้าง Profile อัตโนมัติ
        self.user = User.objects.create_user(username='testuser', password='password123')

        # ดึง Profile ที่สร้างจาก Signal มาใช้งาน
        self.profile = self.user.profile
        self.profile.bio = "Test bio"
        self.profile.faculty = "Engineering"
        self.profile.line = "@testline"
        self.profile.instagram = "test_instagram"
        self.profile.save()
            
    
    


    def test_profile_creation(self):
        # ตรวจสอบว่ามี Profile เชื่อมโยงกับ User
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.bio, 'Test bio')
        self.assertEqual(self.profile.faculty, 'Engineering')

    def test_profile_str_representation(self):
        # ทดสอบ __str__ method
        self.assertEqual(str(self.profile), 'testuser')

    def test_faculty_choices(self):
        # ตรวจสอบว่า faculty ที่เลือกตรงกับ choices
        valid_choices = dict(Profile.FACULTY_CHOICES).keys()
        self.assertIn(self.profile.faculty, valid_choices)

    def test_profile_picture_default(self):
        # ทดสอบค่าเริ่มต้นของ profile_picture
        default_picture = 'profile_picture/default_profile_picture.png'
        self.assertEqual(self.profile.profile_picture.name, default_picture)

    def test_profile_update(self):
        # ทดสอบการแก้ไขข้อมูล Profile
        self.profile.bio = "Updated bio"
        self.profile.save()
        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.bio, "Updated bio")
