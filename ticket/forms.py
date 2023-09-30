# coding=utf-8
from django import forms
from .models import Ticket
from django.contrib.auth.models import User

class AddTicketForm(forms.ModelForm):
    """ Форма добавления тикетов
    """
    class Meta:
        model = Ticket
        fields = ("category", "title", "text")

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
