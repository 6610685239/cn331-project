from django.db import models


class AlertPost(models.Model):
    POST_TYPE_CHOICES = [
        ("caution", "Caution"),
        ("emergency", "Emergency"),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    post_type = models.CharField(max_length=10, choices=POST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.post_type.capitalize()}"
