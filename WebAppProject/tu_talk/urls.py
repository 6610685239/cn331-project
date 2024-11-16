from django.urls import path
from . import views

app_name = "tu_talk"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/new/", views.create_post, name="create_post"),
    path("post/<int:post_id>/like/", views.like_post, name="like_post"),
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),
    path(
        "post/<int:post_id>/comments/",
        views.view_all_comments,
        name="view_all_comments",
    ),
]
