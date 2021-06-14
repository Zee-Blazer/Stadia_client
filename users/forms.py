from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    # email = forms.EmailField()
    GENDER_CHOICES = (
        ('F', 'Female',),
        ('M', 'Male',),
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    agent = forms.BooleanField(required=False)

    def clean(self):
        raise forms.ValidationError({
            "username": "Username already exists!",
            "email": "Email address already exist!"
        })

    class Meta:
        model = User
        fields = 'username', 'email', 'gender', 'password1', 'password2', 'agent'

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for field_name in ['username', 'email', 'gender', 'password1', 'password2', 'agent']:
            self.fields[field_name].help_text = None
