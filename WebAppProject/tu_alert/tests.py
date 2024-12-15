from django.test import TestCase
from django.urls import reverse
from tu_alert.models import AlertPost
from django.utils.timezone import now, timedelta, now


class AlertListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create multiple alert posts
        AlertPost.objects.create(
            title="Caution Alert",
            content="This is a caution alert.",
            post_type="caution",
            created_at=now() - timedelta(days=1),
        )
        AlertPost.objects.create(
            title="Emergency Alert",
            content="This is an emergency alert.",
            post_type="emergency",
            created_at=now(),
        )

    def test_alert_list_view_url_exists(self):
        response = self.client.get("/tu_alert/")
        self.assertEqual(response.status_code, 200)

    def test_alert_list_view_accessible(self):
        response = self.client.get(reverse("tu_alert:alert_list"))
        self.assertEqual(response.status_code, 200)

    def test_alert_list_view_uses_correct_template(self):
        response = self.client.get(reverse("tu_alert:alert_list"))
        self.assertTemplateUsed(response, "tu_alert/alert_list.html")


class AlertPostModelTest(TestCase):
    def test_alert_post_str_method_caution(self):
        alert = AlertPost.objects.create(
            title="Test Alert",
            content="This is a test alert.",
            post_type="caution",
            created_at=now(),
        )
        self.assertEqual(str(alert), "Test Alert - Caution")

    def test_alert_post_str_method_emergency(self):
        alert = AlertPost.objects.create(
            title="Test Alert",
            content="This is a test alert.",
            post_type="emergency",
            created_at=now(),
        )
        self.assertEqual(str(alert), "Test Alert - Emergency")
