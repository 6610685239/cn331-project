from django.urls import path
from .views import *

app_name = "tu_review"

urlpatterns = [
    path("", tu_review, name="tu_review"),

    path('dorm/', DormListView.as_view(), name='dorm_list'),
    path('dorm/<int:dorm_id>/', DormDetailView.as_view(), name='dorm_detail'),
    path('dorm/<int:dorm_id>/review/', DormReviewCreateView.as_view(), name='review_create'),
    path('review/<int:review_id>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('dorm_create/', DormCreateView.as_view(), name='dorm_create_create'),

    path('study/', study, name='study'),
    path('faculty/<int:faculty_id>/', faculty_view, name='faculty'),
    path('faculty/<int:faculty_id>/add-review/', add_review_view, name='add_review'),
    path('review/<int:review_id>/delete/', delete_review_view, name='delete_review'),

    path('restaurant/', restaurant_list, name='restaurant_list'),
    path('restaurant/<int:restaurant_id>/', restaurant_detail, name='restaurant_detail'),
    path('restaurant/<int:restaurant_id>/review/', post_review, name='post_review'),
]


