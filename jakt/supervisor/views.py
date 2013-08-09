# coding=utf-8
"""Supervisor views."""
import logging, random
logger = logging.getLogger(__name__)

# Django imports
from django.core import signing
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate as dj_authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Project imports
from utility import annoying as a
from utility import emails

# Internal imports
from .models import User
from .forms import LoginForm, SignupForm

def signup (request):
    form = SignupForm()
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User(**form.cleaned_data)
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            user = dj_authenticate(username=user.username, password=form.cleaned_data.get("password"))
            if user and user.is_active:
                dj_login(request, user)
                return HttpResponseRedirect("/")
    return render(request, "supervisor/signup.html", {"form" : form})

def login (request, out=None):
    if request.GET.get("next", None):
        request.session["next-url"] = request.GET.get("next")

    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    if out:
        return HttpResponseRedirect(singly.http.connect(out, redirect_uri=request.build_absolute_uri(reverse("sv-bounce"))))
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            dj_login(request, form.cleaned_data.get("user"))
            request.session["timezone"] = a.default_if_none(request.user.timezone, settings.TIME_ZONE)
            next = request.session.get("next-url")
            if next:
                del request.session["next-url"]
            else:
                next = "/"
            return HttpResponseRedirect(next)
    return render(request, "supervisor/login.html", { "form" : form })

def logout (request):
    dj_logout(request)
    return HttpResponseRedirect("/")