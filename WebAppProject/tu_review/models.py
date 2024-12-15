from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View

# Models
class Dormitory(models.Model):
    name = models.CharField(max_length=255)
    location = models.TextField()
    image = models.ImageField(upload_to='dorm_images/')
    description = models.TextField()
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class DormRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.TextField()
    image = models.ImageField(upload_to='dorm_request_images/', blank=True, null=True)
    description = models.TextField()
    recommendation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"{self.name} by {self.user.username}"

class DormReview(models.Model):
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image_or_video = models.FileField(upload_to='review_media/', blank=True, null=True)
    anonymous = models.BooleanField(default=False)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField() 

    def __str__(self):
        return self.title

#study 
class Faculty(models.Model):
    name_th = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    description = models.TextField()
    established_date = models.DateField()
    color = models.CharField(max_length=7)  # Hex color code
    logo = models.ImageField(upload_to='faculty_logos/')

    def __str__(self):
        return self.name_en

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='courses')

    def __str__(self):
        return f"{self.code} - {self.name}"

class StudyReview(models.Model):
    COURSE_TYPES = [
        ('core', 'วิชาเฉพาะ'),
        ('gen_ed', 'วิชาศึกษาทั่วไป'),
        ('elective', 'วิชาเลือกเสรี'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
   
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='reviews')
    instructor = models.CharField(max_length=255)
    semester = models.IntegerField(choices=[(i, i) for i in range(1, 3)])  # Rating for the restaurant (1-5)
    details = models.TextField()
    course_type = models.CharField(max_length=10, choices=COURSE_TYPES)
    interest = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating for the restaurant (1-5)
    practical_use = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating for the restaurant (1-5)
    future_use = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating for the restaurant (1-5)
    instructor_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating for the restaurant (1-5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.code} by {self.user.username}"
    
#resturant
class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    # Add more fields like description, etc. if needed

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='menu_items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class RestaurantReview(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating for the restaurant (1-5)
    cleanliness_rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Cleanliness rating (1-5)
    menu_rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])  # Rating for menu item (1-5)
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user} for {self.restaurant}"