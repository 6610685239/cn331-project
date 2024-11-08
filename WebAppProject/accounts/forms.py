from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),  # Added placeholder here
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )  # Added placeholder here
    )


class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=10,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Username(รหัสนักศึกษา)"}),
    )
    email = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "Email"}),
    )

    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # ตรวจสอบรูปแบบ email
        if not re.match(r"^[\w\.-]+@dome\.tu\.ac\.th$", email):
            raise ValidationError("โปรดใช้ email มหาวิทยาลัยธรรมศาสตร์ ")
        return email
