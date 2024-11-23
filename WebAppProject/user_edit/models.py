from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    FACULTY_CHOICES = [
    ("Law", "Faculty of Law"),
    ("Commerce and Accountancy", "Faculty of Commerce and Accountancy"),
    ("Political Science", "Faculty of Political Science"),
    ("Economics", "Faculty of Economics"),
    ("Social Administration", "Faculty of Social Administration"),
    ("Liberal Arts", "Faculty of Liberal Arts"),
    ("Journalism and Mass Communication", "Faculty of Journalism and Mass Communication"),
    ("Sociology and Anthropology", "Faculty of Sociology and Anthropology"),
    ("Science and Technology", "Faculty of Science and Technology"),
    ("Engineering", "Faculty of Engineering"),
    ("Medicine", "Faculty of Medicine"),
    ("Public Health", "Faculty of Public Health"),
    ("Allied Health Sciences", "Faculty of Allied Health Sciences"),
    ("Nursing", "Faculty of Nursing"),
    ("Architecture and Planning", "Faculty of Architecture and Planning"),
    ("Fine and Applied Arts", "Faculty of Fine and Applied Arts"),
    ("Learning Sciences and Education", "Faculty of Learning Sciences and Education"),
    ("Innovation in Social Sciences", "Faculty of Innovation in Social Sciences"),
    ("Pridi Banomyong International College", "Pridi Banomyong International College"),
    ("College of Interdisciplinary Studies", "College of Interdisciplinary Studies"),
    ("School of Global Studies", "School of Global Studies"),
    ("Chulabhorn International College of Medicine", "Chulabhorn International College of Medicine"),
    ("College of Innovation", "College of Innovation"),
    ("Sirindhorn International Institute of Technology", "Sirindhorn International Institute of Technology"),
]
    faculty = models.CharField(max_length=255, choices=FACULTY_CHOICES, blank=True)
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