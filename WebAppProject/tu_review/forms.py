from django import forms
from .models import *

class DormitoryCreateForm(forms.ModelForm):
    class Meta:
        model = Dormitory
        fields = ['name', 'location', 'image', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter dorm name'}),
            'location': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
        }

class DormReviewForm(forms.ModelForm):
    class Meta:
        model = DormReview
        fields = ['title', 'content', 'rating', 'anonymous']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter review title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your review here'}),
            'rating': forms.Select(attrs={'class': 'form-control'}, choices=[(i, i) for i in range(1, 6)]),
            'anonymous': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

#study
    
class StudyReviewForm(forms.ModelForm):
    class Meta:
        model = StudyReview
        fields = ['course', 'instructor', 'semester', 'details', 'course_type', 'interest', 'practical_use', 'future_use', 'instructor_rating']

#resturant

class ResturantReviewForm(forms.ModelForm):
    class Meta:
        model = RestaurantReview
        fields = ['restaurant','review_text', 'rating', 'cleanliness_rating', 'menu_rating', 'image']
        widgets = {
            'review_text': forms.Textarea(attrs={'rows': 5}),
        }

