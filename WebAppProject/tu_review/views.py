from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path
from django import forms
from django.contrib import admin
from django.db.models import Avg

def tu_review(request):
    return render(request, 'gateway.html')

# dorm
class DormListView(View):
    def get(self, request):
        dorms = Dormitory.objects.all().order_by('-average_rating')
        return render(request, 'dorm_list.html', {'dorms': dorms})

class DormDetailView(View):
    def get(self, request, dorm_id):
        dorm = get_object_or_404(Dormitory, id=dorm_id)
        reviews = dorm.reviews.all()
        return render(request, 'dorm_detail.html', {'dorm': dorm, 'reviews': reviews})

class DormReviewCreateView(View):
    def post(self, request, dorm_id):
        dorm = get_object_or_404(Dormitory, id=dorm_id)
        title = request.POST['title']
        content = request.POST['content']
        rating = int(request.POST['rating'])
        anonymous = 'anonymous' in request.POST
        review = DormReview.objects.create(
            dormitory=dorm,
            user=request.user,
            title=title,
            content=content,
            rating=rating,
            anonymous=anonymous
        )

        # Update average rating
        reviews = dorm.reviews.all()
        dorm.average_rating = sum(r.rating for r in reviews) / len(reviews)
        dorm.save()

        return redirect('tu_review:dorm_detail', dorm_id=dorm.id)

class ReviewDeleteView(View):
    def post(self, request, review_id):
        review = get_object_or_404(DormReview, id=review_id, user=request.user)
        review.delete()

        # Update average rating
        dorm = review.dormitory
        reviews = dorm.reviews.all()
        dorm.average_rating = sum(r.rating for r in reviews) / len(reviews) if reviews else 0.0
        dorm.save()

        return redirect('tu_review:dorm_detail', dorm_id=dorm.id)

class DormCreateView(View):
    def get(self, request):
        form = DormitoryCreateForm()
        return render(request, 'dorm_create_form.html', {'form': form})

    def post(self, request):
        form = DormitoryCreateForm(request.POST, request.FILES)
        if form.is_valid():
            dorm = form.save()
            return redirect('tu_review:dorm_list')  # Redirect ไปยังหน้ารายการหอพัก
        return render(request, 'dorm_create_form.html', {'form': form})

#study

def study(request):
    faculties = Faculty.objects.all()
    top_courses = Course.objects.annotate(
        avg_rating=Avg('reviews__interest')
    ).order_by('-avg_rating')[:3]
    return render(request, 'study.html', {'faculties': faculties, 'top_courses': top_courses})

def faculty_view(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    courses = faculty.courses.all()
    return render(request, 'study_faculty.html', {'faculty': faculty, 'courses': courses})

@login_required
def add_review_view(request, faculty_id):
    faculty = get_object_or_404(Faculty, id=faculty_id)
    if request.method == 'POST':
        form = StudyReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('tu_review:faculty', faculty_id=faculty.id)
    else:
        form = StudyReviewForm()
    return render(request, 'study_add_review.html', {'form': form, 'faculty': faculty})

@login_required
def delete_review_view(request, review_id):
    review = get_object_or_404(StudyReview, id=review_id, user=request.user)
    review.delete()
    return JsonResponse({'success': True})


#resturant
# View to list restaurants
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    # Get top 3 restaurants with the highest average rating
    top_restaurants = Restaurant.objects.annotate(avg_rating=models.Avg('reviews__rating')).order_by('-avg_rating')[:3]
    return render(request, 'restaurant_list.html', {'restaurants': restaurants, 'top_restaurants': top_restaurants})

# View to see restaurant details and reviews
def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    reviews = restaurant.reviews.all()
    return render(request, 'restaurant_detail.html', {'restaurant': restaurant, 'reviews': reviews})

# View to post a review
def post_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    if request.method == 'POST':
        form = ResturantReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.restaurant = restaurant
            review.user = request.user
            review.save()
            return redirect('tu_review:restaurant_detail', restaurant_id=restaurant.id)
    else:
        form = ResturantReviewForm()

    return render(request, 'restaurant_post_review.html', {'form': form, 'restaurant': restaurant})