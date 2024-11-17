from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Like
from .forms import PostForm, CommentForm
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from django.core.exceptions import ValidationError
from .models import validate_image_extension


class TuTalkTests(TestCase):

    def setUp(self):
        """Set up initial test data."""
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="zazazaza")
        self.user2 = User.objects.create_user(
            username="otheruser", password="zazazaza1"
        )
        self.post = Post.objects.create(user=self.user, content="Test Post")
        self.comment = Comment.objects.create(
            user=self.user, post=self.post, content="Test Comment"
        )
        self.like_url = reverse("tu_talk:like_post", args=[self.post.id])
        self.comment_url = reverse("tu_talk:add_comment", args=[self.post.id])
        self.view_all_comments_url = reverse(
            "tu_talk:view_all_comments", args=[self.post.id]
        )

    ### View Tests ###

    def test_post_list_view(self):
        """Test the post list view."""
        self.client.login(username="testuser", password="zazazaza")
        response = self.client.get(reverse("tu_talk:post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.content)

    def test_create_post_view_get(self):
        """Test create post GET request."""
        self.client.login(username="testuser", password="zazazaza")
        response = self.client.get(reverse("tu_talk:create_post"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tu_talk/create_post.html")

    def test_create_post_view_post_user_association(self):
        """Test that the created post is associated with the logged-in user."""
        self.client.login(username="testuser", password="zazazaza")

        image_io = BytesIO()
        image = Image.new("RGB", (100, 100), color="green")  # Green square image
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "test.jpg", image_io.read(), content_type="image/jpeg"
        )

        # Send the POST request
        response = self.client.post(
            reverse("tu_talk:create_post"),
            {
                "content": "Post by testuser",
                "image": uploaded_image,
            },
        )

        # Ensure the post is saved and associated with the correct user
        post = Post.objects.last()
        self.assertEqual(post.user, self.user)
        self.assertEqual(Post.objects.count(), 2)  # Ensure a new post was created

    def test_add_comment_view_get(self):
        """Test GET request to add a comment."""
        self.client.login(username="testuser", password="zazazaza")

        # Send GET request to add comment view
        response = self.client.get(self.comment_url)

        # Assert that the response status is 200 OK
        self.assertEqual(response.status_code, 200)

        # Ensure the form is in the context (line 52)
        self.assertIn("form", response.context)

        # Ensure the post object is in the context (line 53)
        self.assertEqual(response.context["post"], self.post)

        # Ensure the correct template is used
        self.assertTemplateUsed(response, "tu_talk/add_comment.html")

    def test_add_comment_view_post(self):
        """Test POST request to add a comment (valid form submission)."""
        self.client.login(username="testuser", password="zazazaza")

        # Send a POST request with comment data
        response = self.client.post(self.comment_url, {"content": "New Comment"})

        # Assert that the response status is a redirect (302)
        self.assertEqual(response.status_code, 302)

        # Ensure a new comment is created
        self.assertEqual(Comment.objects.count(), 2)

        # Verify that the new comment is correctly associated with the post and user
        comment = Comment.objects.last()
        self.assertEqual(comment.content, "New Comment")
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.user, self.user)

    def test_like_post_view(self):
        """Test liking a post."""
        self.client.login(username="testuser", password="zazazaza")
        response = self.client.get(self.like_url)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Like.objects.filter(post=self.post, user=self.user).count(), 1)

    def test_like_post_view_already_liked(self):
        """Test that liking the post twice will unlike it."""
        self.client.login(username="testuser", password="zazazaza")

        # Like the post
        self.client.get(self.like_url)  # First like
        self.assertEqual(Like.objects.filter(post=self.post, user=self.user).count(), 1)

        # Like again, it should be unliked
        self.client.get(self.like_url)  # Unlike
        self.assertEqual(Like.objects.filter(post=self.post, user=self.user).count(), 0)

    def test_unlike_post_view(self):
        """Test unliking a post."""
        self.client.login(username="testuser", password="zazazaza")
        Like.objects.create(post=self.post, user=self.user)
        response = self.client.get(self.like_url)
        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertEqual(Like.objects.filter(post=self.post, user=self.user).count(), 0)

    def test_view_all_comments_view(self):
        """Test viewing all comments."""
        self.client.login(username="testuser", password="zazazaza")
        response = self.client.get(self.view_all_comments_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.comment.content)

    def test_view_all_comments_view_multiple(self):
        """Test viewing all comments when there are multiple comments."""
        self.client.login(username="testuser", password="zazazaza")

        # Add a second comment
        Comment.objects.create(
            user=self.user2, post=self.post, content="Another comment"
        )

        response = self.client.get(self.view_all_comments_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Another comment")  # Check for the second comment

    ### Model Tests ###

    def test_post_model(self):
        """Test Post model."""
        self.assertEqual(str(self.post), "testuser's Post - Test Post")

    def test_comment_model(self):
        """Test Comment model."""
        self.assertEqual(str(self.comment), "testuser - Comment on 1")

    def test_like_model(self):
        """Test Like model."""
        like = Like.objects.create(post=self.post, user=self.user)
        self.assertEqual(str(like), "testuser liked Post 1")

    def test_valid_image_extension(self):
        """Test that valid image extensions do not raise validation errors."""

        # Create a valid .jpg image
        image_io = BytesIO()
        image = Image.new("RGB", (100, 100), color="red")
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "test.jpg", image_io.read(), content_type="image/jpeg"
        )

        try:
            # Test that no validation error is raised
            validate_image_extension(uploaded_image)
        except ValidationError:
            self.fail("ValidationError raised for valid image (.jpg)")

    def test_invalid_image_extension(self):
        """Test that invalid image extensions raise a ValidationError."""

        # Create an invalid .txt file
        text_io = BytesIO(b"This is a text file, not an image.")
        text_file = SimpleUploadedFile(
            "test.txt", text_io.read(), content_type="text/plain"
        )

        with self.assertRaises(ValidationError):
            # Test that a ValidationError is raised for an invalid file extension
            validate_image_extension(text_file)

    def test_other_valid_image_extensions(self):
        """Test other valid image extensions."""

        # Valid PNG image
        image_io = BytesIO()
        image = Image.new("RGB", (100, 100), color="blue")
        image.save(image_io, format="PNG")
        image_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "test.png", image_io.read(), content_type="image/png"
        )

        try:
            # Test that no validation error is raised for .png
            validate_image_extension(uploaded_image)
        except ValidationError:
            self.fail("ValidationError raised for valid image (.png)")

        # Valid GIF image
        image_io = BytesIO()
        image = Image.new("RGB", (100, 100), color="green")
        image.save(image_io, format="GIF")
        image_io.seek(0)

        uploaded_image = SimpleUploadedFile(
            "test.gif", image_io.read(), content_type="image/gif"
        )

        try:
            # Test that no validation error is raised for .gif
            validate_image_extension(uploaded_image)
        except ValidationError:
            self.fail("ValidationError raised for valid image (.gif)")

    ### Form Tests ###

    def test_post_form_valid(self):
        """Test PostForm with valid data."""
        # Create a valid in-memory image
        image_io = BytesIO()
        image = Image.new("RGB", (100, 100), color="red")  # A simple red square image
        image.save(image_io, format="JPEG")
        image_io.seek(0)

        # Create a SimpleUploadedFile from the image
        uploaded_image = SimpleUploadedFile(
            "test.jpg", image_io.read(), content_type="image/jpeg"
        )

        # Create the form with valid data
        form = PostForm(
            data={"content": "Valid Content"}, files={"image": uploaded_image}
        )

        # Assert that the form is valid
        self.assertTrue(form.is_valid(), msg=form.errors)

        # Save the form instance
        post = form.save(commit=False)
        post.user = self.user  # Assign the user
        post.save()

        # Verify the saved post
        self.assertEqual(post.content, "Valid Content")
        self.assertIsNotNone(post.image)  # Ensure the image was saved

    def test_post_form_invalid(self):
        """Test PostForm with invalid data."""
        form = PostForm(data={})
        self.assertFalse(form.is_valid())

    def test_comment_form_valid(self):
        """Test CommentForm with valid data."""
        form = CommentForm(data={"content": "Valid Comment"})
        self.assertTrue(form.is_valid())

    def test_comment_form_invalid(self):
        """Test CommentForm with invalid data."""
        form = CommentForm(data={})
        self.assertFalse(form.is_valid())

    ### URL Tests ###

    def test_urls_resolve_correctly(self):
        """Test if URLs resolve to correct views."""
        self.assertEqual(reverse("tu_talk:post_list"), "/tu_talk/")
        self.assertEqual(reverse("tu_talk:create_post"), "/tu_talk/post/new/")
        self.assertEqual(
            reverse("tu_talk:add_comment", args=[self.post.id]),
            f"/tu_talk/post/{self.post.id}/comment/",
        )
        self.assertEqual(
            reverse("tu_talk:like_post", args=[self.post.id]),
            f"/tu_talk/post/{self.post.id}/like/",
        )
        self.assertEqual(
            reverse("tu_talk:view_all_comments", args=[self.post.id]),
            f"/tu_talk/post/{self.post.id}/comments/",
        )
