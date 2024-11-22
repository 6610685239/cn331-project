from django.db import models
from django.contrib.auth.models import User


class Party(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="parties")
    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField()
    image = models.ImageField(upload_to="parties/images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.event_date}"


class PartyInterest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="interests")
    party = models.ForeignKey(
        Party, on_delete=models.CASCADE, related_name="interested_users"
    )

    def __str__(self):
        return f"{self.user.username} is interested in {self.party.title}"
