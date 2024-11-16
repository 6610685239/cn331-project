from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_image_extension(value):
    if not value.name.endswith((".jpg", ".jpeg", ".png")):
        raise ValidationError("Only .jpg and .png files are allowed.")


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    image = models.ImageField(
        upload_to="posts/images/",
        blank=True,
        null=True,
        validators=[validate_image_extension],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Post - {self.content[:20]}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Comment on {self.post.id}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked Post {self.post.id}"
