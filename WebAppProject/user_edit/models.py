from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    faculty = models.TextField(blank=True)  # Ensure this field exists
    line = models.TextField(blank=True)
    instagram = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to='profile_picture/',
        blank=True,
        null=True,
        default='profile_picture/default_profile_picture.png'  # Path to default profile picture
    )

    def __str__(self):
        return self.user.username