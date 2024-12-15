from django import forms
from .models import *

class DormReviewForm(forms.ModelForm):
    class Meta:
        model = DormReview
        fields = ['rating', 'comment']

    
class StudyReviewForm(forms.ModelForm):
    class Meta:
        model = StudyReview
        fields = ['course', 'instructor', 'semester', 'details', 'course_type', 'interest', 'practical_use', 'future_use', 'instructor_rating']

#resturant

class ResturantReviewForm(forms.ModelForm):
    class Meta:
        model = RestaurantReview
        fields = ['review_text', 'rating', 'cleanliness_rating', 'menu_rating', 'image']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 5}),
        }