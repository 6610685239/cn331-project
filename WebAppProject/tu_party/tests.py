from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Party, PartyInterest
from django.utils.timezone import now, timedelta
from django.db import IntegrityError



class PartyTests(TestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.login(username="testuser", password="password")
        
        # Create sample party
        self.party = Party.objects.create(
            user=self.user,
            title="Test Party",
            description="A fun test party",
            event_date=now().date() + timedelta(days=1),
            event_time="18:00",
        )

    def test_party_list_view(self):
        response = self.client.get(reverse("tu_party:party_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tu_party/party_list.html")
        self.assertContains(response, "Test Party")

    def test_create_party_view_get(self):
        response = self.client.get(reverse("tu_party:create_party"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tu_party/create_party.html")

    def test_create_party_view_post(self):
        data = {
            "title": "New Party",
            "description": "Exciting event",
            "event_date": (now().date() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "event_time": "20:00",
        }
        response = self.client.post(reverse("tu_party:create_party"), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Party.objects.filter(title="New Party").exists())

    def test_interest_party_view_create(self):
        response = self.client.post(reverse("tu_party:interest_party", args=[self.party.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to party list
        self.assertTrue(PartyInterest.objects.filter(party=self.party, user=self.user).exists())

    def test_interest_party_view_delete(self):
        # Create interest first
        PartyInterest.objects.create(party=self.party, user=self.user)
        response = self.client.post(reverse("tu_party:interest_party", args=[self.party.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to party list
        self.assertFalse(PartyInterest.objects.filter(party=self.party, user=self.user).exists())

    def test_party_list_only_upcoming_events(self):
        # Create past party
        Party.objects.create(
            user=self.user,
            title="Past Party",
            description="A past event",
            event_date=now().date() - timedelta(days=1),
            event_time="18:00",
        )
        response = self.client.get(reverse("tu_party:party_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Party")
        self.assertNotContains(response, "Past Party")





class PartyModelTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="password")
        # Create a party
        self.party = Party.objects.create(
            user=self.user,
            title="Test Party",
            description="A fun test party",
            event_date=now().date() + timedelta(days=1),
            event_time="18:00",
        )

    def test_party_str_method(self):
        # Test the __str__ method of Party
        self.assertEqual(str(self.party), f"Test Party - {self.party.event_date}")

    def test_party_creation(self):
        # Test that Party was created with correct fields
        self.assertEqual(self.party.user, self.user)
        self.assertEqual(self.party.title, "Test Party")
        self.assertEqual(self.party.description, "A fun test party")
        self.assertEqual(self.party.event_date, now().date() + timedelta(days=1))
        self.assertEqual(self.party.event_time, "18:00")
        # ทดสอบฟิลด์ image ว่าไม่มีค่า
        self.assertFalse(self.party.image.name)  # จะเป็น empty string หากไม่มีค่า


class PartyInterestModelTests(TestCase):
    def setUp(self):
        # Create a user and party
        self.user = User.objects.create_user(username="testuser", password="password")
        self.party = Party.objects.create(
            user=self.user,
            title="Test Party",
            description="A fun test party",
            event_date=now().date() + timedelta(days=1),
            event_time="18:00",
        )
        # Create a PartyInterest instance
        self.interest = PartyInterest.objects.create(user=self.user, party=self.party)

    def test_partyinterest_str_method(self):
        # Test the __str__ method of PartyInterest
        self.assertEqual(
            str(self.interest),
            f"{self.user.username} is interested in {self.party.title}",
        )

    def test_partyinterest_creation(self):
        # Test that PartyInterest was created correctly
        self.assertEqual(self.interest.user, self.user)
        self.assertEqual(self.interest.party, self.party)

    def test_partyinterest_uniqueness(self):
        with self.assertRaises(IntegrityError):
            PartyInterest.objects.create(user=self.user, party=self.party)
