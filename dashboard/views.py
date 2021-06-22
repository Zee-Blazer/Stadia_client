from .utilities import *
from . import models, forms
from django.db.models import Q
from django.urls import reverse
from django.contrib import messages
from users.models import UserProfile
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


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
        form = forms.UserForm(request.POST)
        password_form = PasswordChangeForm(request.user, request.POST)

        if password_form.is_valid():
            user = password_form.save()

            update_session_auth_hash(request, user)  # Important!

            message = 'Your password was successfully updated!'
            messages.success(request, message)
        elif form.is_valid():
            form.save()

            message = f"Your profile has successfully been updated!"
            messages.success(request, message)
        else:
            message = "Profile information change failed!"
            messages.error(request, message)

        return redirect('user_dashboard:profile')
    else:
        form = forms.UserForm(instance=user)
        password_form = PasswordChangeForm(request.user)

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
        form = forms.EventForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            name, dis_image, capacity, description, price, date = (
                cd['name'], cd['image'], cd['capacity'],
                cd['description'], cd['price'], cd['date'],
            )

            date = DateTimeHandler(date)

            models.Event.objects.create(
                event_creator=user_profile, name=name, slug=slugify(name), dis_image=dis_image,
                capacity=capacity, description=description, price=price, date=date.datetime
            ).save()

            message = f"Your event has successfully been created!"
            messages.success(request, message)

            return redirect('user_dashboard:dashboard')
        else:
            message = f"Your event could not be created! Perhaps you didn't fill the form accurately enough."
            messages.error(request, message)
    else:
        form = forms.EventForm()

    context = {
        'user': user,
        'user_profile': user_profile,
        'form': form,
        'value': "Create Event"
    }

    return render(request, 'dashboard/files/create_event.html', context)


def created_events(request):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)
    events = models.Event.objects.filter(event_creator=user_profile)

    context = {
        'user': user,
        'user_profile': user_profile,
        'events': events,
    }

    return render(request, 'dashboard/files/created_events.html', context)


def edit_event(request, event_id):
    user = User.objects.get(username=request.user.username)
    user_profile = UserProfile.objects.get(user=user)

    event = models.Event.objects.get(id=event_id)
    event_form = forms.EventForm(instance=event)

    context = {
        'user': user,
        'user_profile': user_profile,
        'form': event_form,
        'value': "Edit Event"
    }

    return render(request, 'dashboard/files/create_event.html', context)


def delete_event(request, event_id):
    event = models.Event.objects.get(id=event_id)
    event.delete()

    message = f"Your event has successfully been deleted!"
    messages.success(request, message)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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
