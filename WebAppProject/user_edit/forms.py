from django import forms
from .models import Profile
from django.contrib.auth.models import User

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio','display_name', 'faculty', 'line', 'instagram', 'profile_picture']  # Ensure faculty exists
