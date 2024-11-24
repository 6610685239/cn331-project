from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Party, PartyInterest
from django.utils.timezone import now, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseForbidden


class TuPartyTests(TestCase):
    def setUp(self):
        # Create users
        self.user = User.objects.create_user(username="testuser", password="password")
        self.other_user = User.objects.create_user(
            username="otheruser", password="password"
        )

        # Create a party
        self.party = Party.objects.create(
            user=self.user,
            title="Test Party",
            description="This is a test party.",
            event_date=now().date() + timedelta(days=1),
            event_time="18:00",
            image=None,
        )

        # Initialize the client
        self.client = Client()

    ### Models Tests ###
    def test_party_str(self):
        self.assertEqual(
            str(self.party), f"{self.party.title} - {self.party.event_date}"
        )

    def test_party_interest_str(self):
        interest = PartyInterest.objects.create(user=self.other_user, party=self.party)
        self.assertEqual(
            str(interest),
            f"{interest.user.username} is interested in {interest.party.title}",
        )

    ### Views Tests ###
    def test_party_list_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("tu_party:party_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tu_party/party_list.html")
        self.assertIn("parties", response.context)

    def test_create_party_view_get(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("tu_party:create_party"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tu_party/create_party.html")

    def test_create_party_view_post(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("tu_party:create_party"),
            {
                "title": "New Party",
                "description": "Description",
                "event_date": now().date() + timedelta(days=2),
                "event_time": "19:00",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Party.objects.filter(title="New Party").exists())

    def test_interest_party_view_add_interest(self):
        self.client.login(username="otheruser", password="password")
        response = self.client.get(
            reverse("tu_party:interest_party", args=[self.party.id])
        )
        self.assertEqual(response.status_code, 302)  # Redirect after toggling interest
        self.assertTrue(
            PartyInterest.objects.filter(
                user=self.other_user, party=self.party
            ).exists()
        )

    def test_interest_party_view_remove_interest(self):
        PartyInterest.objects.create(user=self.other_user, party=self.party)
        self.client.login(username="otheruser", password="password")
        response = self.client.get(
            reverse("tu_party:interest_party", args=[self.party.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            PartyInterest.objects.filter(
                user=self.other_user, party=self.party
            ).exists()
        )

    def test_interested_users_view_allowed(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(
            reverse("tu_party:interested_users", args=[self.party.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tu_party/interested_users.html")

    def test_interested_users_view_forbidden(self):
        self.client.login(username="otheruser", password="password")
        response = self.client.get(
            reverse("tu_party:interested_users", args=[self.party.id])
        )
        self.assertEqual(response.status_code, 403)  # Forbidden for non-creator users

    ### URLs Tests ###
    def test_urls(self):
        self.assertEqual(reverse("tu_party:party_list"), "/tu_party/")
        self.assertEqual(reverse("tu_party:create_party"), "/tu_party/create/")
        self.assertEqual(
            reverse("tu_party:interest_party", args=[self.party.id]),
            f"/tu_party/{self.party.id}/interest/",
        )
        self.assertEqual(
            reverse("tu_party:interested_users", args=[self.party.id]),
            f"/tu_party/party/{self.party.id}/interested-users/",
        )
