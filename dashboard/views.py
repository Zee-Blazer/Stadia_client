from django.shortcuts import render, redirect
from users.models import UserProfile
from . import models, forms
from .utilities import *
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User


def dashboard(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    events = models.Event.objects.all()
    tickets = models.Ticket.objects.filter(attendee=user_profile)

    # This program will not scale with a huge number of events
    # As such should be upgraded before deployment
    events = [event for event in events if event not in [ticket.event for ticket in tickets]]

    if len(events) > 6:
        events = events[:6]

    context = {
        'user': user,
        'user_profile': user_profile,
        'events': events,
        'tickets': tickets,
    }

    return render(request, 'dashboard/files/dashboard.html', context)


def all_events(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    events = models.Event.objects.all()
    tickets = models.Ticket.objects.filter(attendee=user_profile)

    # This program will not scale with a huge number of events
    # As such should be upgraded before deployment
    events = [event for event in events if event not in [ticket.event for ticket in tickets]]

    context = {
        'user': user,
        'user_profile': user_profile,
        'events': events,
    }

    return render(request, 'dashboard/files/all_events.html', context)


def programs(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    tickets = models.Ticket.objects.filter(attendee=user_profile)

    context = {
        'user': user,
        'user_profile': user_profile,
        'tickets': tickets,
    }

    return render(request, 'dashboard/files/programs.html', context)


def view_ticket(request, ticket_id):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    ticket = models.Ticket.objects.get(id=ticket_id)

    date = ticket.event.date.date()
    time = ticket.event.date.time()

    date = f"{date.day}{day_prefix_setter(date.day)}/{month_setter(date.month)}/{date.year}"
    time = f"{time.hour}:{time.minute}"

    context = {
        'user': user,
        'user_profile': user_profile,
        'ticket': ticket,
        'date': date,
        'time': time,
    }

    return render(request, 'dashboard/files/ticket.html', context)


def search(request):
    query = request.GET.get('q')

    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)

    context = {
        'user': user,
        'user_profile': user_profile,
    }

    if query is not None:
        events = models.Event.objects.filter(Q(name__icontains=query))
        context['events'] = events

    return render(request, 'dashboard/files/search.html', context)


def profile(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        password_form = forms.UserPasswordChangeForm(request.POST)
        form = forms.UserForm(request.POST)
        if form.is_valid():
            form.save()

            message = f"Your profile has successfully been updated!"
            messages.success(request, message)

        if password_form.is_valid():
            form.save()

            message = f"Your password has successfully been changed!"
            messages.success(request, message)

        return redirect('user_dashboard:profile')
    else:
        form = forms.UserForm(instance=user)
        password_form = forms.UserPasswordChangeForm(user)

    context = {
        'user': user,
        'user_profile': user_profile,
        'form': form,
        'password_form': password_form,
    }
    return render(request, 'dashboard/files/profile.html', context)


def create_event(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        form = forms.EventForm(request.post)
        if form.is_valid():
            form.save()

            message = f"Your event has successfully been created!"
            messages.success(request, message)

            return redirect('user_dashboard:dashboard')
    else:
        form = forms.EventForm()

    context = {
        'user': user,
        'user_profile': user_profile,
        'form': form,
    }

    return render(request, 'dashboard/files/create_event.html', context)


def add_event(request, event_name):
    event = models.Event.objects.get(name=event_name)

    if event.can_book_seat():
        user = User.objects.get(username=request.user.username)
        user_profile = UserProfile.objects.get(user=user)

        date = event.date.date()
        time = event.date.time()

        date = f"{date.day}{day_prefix_setter(date.day)}/{month_setter(date.month)}/{date.year}"
        time = f"{time.hour}:{time.minute}"

        if request.method == 'POST':
            form = forms.AttendTicketForm(request.POST)
            if form.is_valid():
                seats = form.cleaned_data.get('book_seat')

                ticket = models.Ticket.objects.create(
                    event=event,
                    attendee=user_profile,
                    book_seat=seats,
                )

                request.session['order_id'] = ticket.id
                request.session['event_id'] = event.id
                request.session['seats'] = seats
                # redirect for payment
                return redirect(reverse('payment:process'))
        else:
            form = forms.AttendTicketForm()

        context = {
            'user': user,
            'user_profile': user_profile,
            'form': form,
            'event': event,
            'date': date,
            'time': time,
        }

        return render(request, 'dashboard/files/add_event.html', context)

    return redirect('user_dashboard:dashboard')
