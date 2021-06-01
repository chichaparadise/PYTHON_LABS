from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from django.forms.models import fields_for_model
from django.forms.widgets import EmailInput
from django.shortcuts import render

from .models import *

class SignInForm(forms.ModelForm):

    username = forms.CharField(widget=forms.TextInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User {username} not found')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect password')
        return self.cleaned_data

    class Meta:

        model = User
        fields = ['username', 'password']


class SignUpForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput, required=False)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Password'
        self.fields['confirm_password'].label = 'Confirm Password'
        self.fields['email'].label = 'Email'
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        # self.fields['phone'].label = 'Phone Number'
        # self.fields['address'].label = 'Address'



    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'User with username "{username}" already exists')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return self.cleaned_data

    class Meta:
        
        model = User
        fields = ['username', 'password', 'confirm_password', 'first_name', 'last_name', 'address', 'phone', 'email']


class AddOfferForm(forms.ModelForm):

    class Meta:   
        model = Offer
        fields = fields_for_model(model)
        exclude = ['owner', 'statistics']