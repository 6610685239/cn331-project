from django.shortcuts import render
from .models import AlertPost


def alert_list(request):
    alerts = AlertPost.objects.order_by("-created_at")
    return render(request, "tu_alert/alert_list.html", {"alerts": alerts})
