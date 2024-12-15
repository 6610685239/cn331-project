from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import (
    Dormitory,
    DormReview,
    Restaurant,
    Faculty,
    Course,
    RestaurantReview,
    StudyReview,
)
from datetime import date
from django.core.files.uploadedfile import SimpleUploadedFile


class TuReviewTests(TestCase):
    def test_tu_review_view(self):
        response = self.client.get(reverse("tu_review:tu_review"))

        self.assertTemplateUsed(response, "gateway.html")


class DormitoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.dorm = Dormitory.objects.create(
            name="Test Dorm", location="Test Location", description="Test Description"
        )
        self.client.login(username="testuser", password="password")

    def test_dorm_list_view(self):
        response = self.client.get(reverse("tu_review:dorm_list"))

        self.assertContains(response, self.dorm.name)
        self.assertContains(response, self.dorm.location)

    def test_dorm_detail_view(self):
        response = self.client.get(
            reverse("tu_review:dorm_detail", args=[self.dorm.id])
        )

        self.assertContains(response, self.dorm.name)
        self.assertContains(response, self.dorm.location)
        self.assertContains(response, self.dorm.description)

    def test_dorm_create_view(self):
        response = self.client.get(reverse("tu_review:dorm_create_form"))

        # Test POST request to create dorm
        data = {
            "name": "New Dorm",
            "location": "New Location",
            "description": "New Description",
        }
        response = self.client.post(reverse("tu_review:dorm_create_form"), data)

        self.assertEqual(Dormitory.objects.count(), 2)

    def test_dorm_review_creation(self):
        review_data = {
            "title": "Test Review",
            "content": "This is a test review.",
            "rating": 5,
            "anonymous": False,
        }
        response = self.client.post(
            reverse("tu_review:review_create", args=[self.dorm.id]), review_data
        )

        self.assertEqual(DormReview.objects.count(), 1)

    def test_review_deletion(self):
        review = DormReview.objects.create(
            dormitory=self.dorm,
            user=self.user,
            title="Test Review",
            content="Test Content",
            rating=5,
        )
        response = self.client.post(
            reverse("tu_review:review_delete", args=[review.id])
        )

        self.assertEqual(DormReview.objects.count(), 0)


class RestaurantTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant", location="Test Location"
        )
        self.client.login(username="testuser", password="password")

    def test_restaurant_list_view(self):
        response = self.client.get(reverse("tu_review:restaurant_list"))

        self.assertContains(response, self.restaurant.name)
        self.assertContains(response, self.restaurant.location)

    def test_restaurant_detail_view(self):
        response = self.client.get(
            reverse("tu_review:restaurant_detail", args=[self.restaurant.id])
        )

        self.assertContains(response, self.restaurant.name)
        self.assertContains(response, self.restaurant.location)


class FacultyTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faculty = Faculty.objects.create(
            name_en="Test Faculty",
            description="Test Description",
            established_date=date(2000, 1, 1),
        )
        self.course = Course.objects.create(name="Test Course", faculty=self.faculty)
        self.client.login(username="testuser", password="password")

    def test_faculty_view(self):
        response = self.client.get(reverse("tu_review:faculty", args=[self.faculty.id]))

        self.assertContains(response, self.faculty.name_en)
        self.assertContains(response, self.course.name)


class CourseTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.faculty = Faculty.objects.create(
            name_en="Test Faculty",
            description="Test Description",
            established_date=date(2000, 1, 1),
        )
        self.course = Course.objects.create(name="Test Course", faculty=self.faculty)
        self.client.login(username="testuser", password="password")

    def test_course_list_view(self):
        response = self.client.get(reverse("tu_review:study"))

        self.assertContains(response, self.course.name)
