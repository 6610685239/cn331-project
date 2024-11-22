from django.shortcuts import render, get_object_or_404, redirect
from .models import Party, PartyInterest
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now


@login_required
def party_list(request):
    parties = Party.objects.filter(event_date__gte=now().date()).order_by("event_date")
    return render(request, "tu_party/party_list.html", {"parties": parties})


@login_required
def create_party(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        event_date = request.POST.get("event_date")
        event_time = request.POST.get("event_time")
        image = request.FILES.get("image")
        Party.objects.create(
            user=request.user,
            title=title,
            description=description,
            event_date=event_date,
            event_time=event_time,
            image=image,
        )
        return redirect("tu_party:party_list")
    return render(request, "tu_party/create_party.html")


@login_required
def interest_party(request, party_id):
    party = get_object_or_404(Party, id=party_id)
    interest, created = PartyInterest.objects.get_or_create(
        party=party, user=request.user
    )
    if not created:
        interest.delete()
    return redirect("tu_party:party_list")
