# coding=utf-8
"""Supervisor forms."""

import logging, random
logger = logging.getLogger(__name__)

# Django imports
from django import forms
from django.contrib.auth import authenticate as dj_authenticate, login as dj_login

from .models import User
from utility.annoying import get_or_none as gon

class LoginForm (forms.Form):
    username = forms.CharField(max_length=30, label="Username")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean (self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user = dj_authenticate(username=username.strip(), password=password)
            if user and user.is_active:
                cleaned_data["user"] = user
            else:
                raise forms.ValidationError("Invalid username or password")
        return cleaned_data

class SignupForm (forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=255)
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean (self):
        cleaned_data = super(SignupForm, self).clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        if email:
            cleaned_data["email"] = email.strip().lower()
            if gon(User, email=cleaned_data["email"]):
                raise forms.ValidationError("That email address already exists.")
        if username:
            cleaned_data["username"] = username.strip()
            if gon(User, username=cleaned_data["username"]):
                raise forms.ValidationError("That username already exists.")

        return cleaned_data

class EmailForm (forms.Form):
    email = forms.EmailField()
