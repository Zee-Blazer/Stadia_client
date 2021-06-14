from . import forms, models
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login


def gender_image_selector(gender):
    if gender == 'M':
        image = 'images/avatar-male.png'
    else:
        image = 'image/avatar-female.png'

    return image


def signup(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            # Saves form and creates user
            form.save()

            cd = form.cleaned_data
            email = cd['email']

            user = User.objects.get(username=cd['username'])

            # Creates user profile leaving other fields default
            models.UserProfile.objects.create(
                user=user,
                email=email,
                image=gender_image_selector(cd['gender']),
                is_agent=cd['agent'],
            ).save()

            message = f"Your account has successfully been created {cd['username'].capitalize()}!"
            messages.success(request, message)

            login(request, user)

            return redirect('user_dashboard:dashboard')
        else:
            message = f"Your account could not be created!"
            messages.error(request, message)
    else:
        form = forms.UserForm()

    context = {
        'form': form,
    }

    return render(request, 'users/files/signup.html', context)
