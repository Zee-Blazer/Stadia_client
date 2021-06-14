from django.shortcuts import render
from users.models import UserProfile
from django.contrib.auth.models import User


def dashboard(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)

    context = {
        'user': user,
        'user_profile': user_profile
    }

    return render(request, 'dashboard/files/dashboard.html', context)
