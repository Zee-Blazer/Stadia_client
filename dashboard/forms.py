from django import forms
from .models import Ticket, Event
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = 'name', 'dis_image', 'capacity', 'description', 'price', 'date'


class AttendTicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = 'book_seat',

    def __init__(self, *args, **kwargs):
        super(AttendTicketForm, self).__init__(*args, **kwargs)

        self.fields['book_seat'].widget.attrs.update({
            'style': 'background-color: #fff;'
        })


class UserForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = User
        fields = 'username', 'email'

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for field_name in ['username', 'email']:
            self.fields[field_name].help_text = None


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.PasswordInput()
    new_password1 = forms.PasswordInput()
    new_password2 = forms.PasswordInput()
