from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.db.models import Prefetch


@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("tu_talk:post_list")
    else:
        form = PostForm()
    return render(request, "tu_talk/create_post.html", {"form": form})


@login_required
def post_list(request):
    posts = Post.objects.prefetch_related(
        Prefetch("comments", queryset=Comment.objects.order_by("-created_at"))
    ).order_by("-created_at")
    return render(request, "tu_talk/post_list.html", {"posts": posts})


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()  # If like exists, it will be removed (unlike)
    return redirect("tu_talk:post_list")


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect("tu_talk:view_all_comments", post_id=post.id)
    else:
        form = CommentForm()
    return render(request, "tu_talk/add_comment.html", {"form": form, "post": post})


@login_required
def view_all_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.order_by("-created_at")  # Retrieve all comments
    return render(
        request, "tu_talk/view_all_comments.html", {"post": post, "comments": comments}
    )
