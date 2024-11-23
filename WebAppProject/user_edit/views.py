from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserEditForm, ProfileEditForm
from .models import *

@login_required
def profile(request):
    profile = request.user.profile
    profile_picture_url = profile.profile_picture.url if profile.profile_picture else '/static/default_profile_picture.png'

    return render(request, 'user_edit/profile.html', {
        'profile': profile,
        'profile_picture_url': profile_picture_url,
    })
@login_required
def profile_edit(request):
    # Skip profile logic for admin users
    if request.user.is_superuser:
        return redirect('admin:index')  # Redirect to the admin interface

    # Ensure the user has a profile
    if not hasattr(request.user, 'profile'):
        Profile.objects.create(user=request.user)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        profile_form = ProfileEditForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_edit:profile')  # Redirect back to the profile page
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'user_edit/profile_edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

