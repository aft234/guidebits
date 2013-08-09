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
import singly.http
from utility import annoying as a
from utility import emails

# Internal imports
from . import auth
from .models import User
from .forms import EmailForm

def next (request):
    """Method of dubious dependability that handles a redirection."""
    if request.GET.get("next", None):
        request.session["next-url"] = request.GET.get("next")

    default = "/"
    if request.user.is_authenticated():
        default = reverse("product.views.all")
        if request.user.is_staff:
            default = reverse("product.views.management")
        if request.user.email == "blank@twitterlogin.com":
            default = reverse("supervisor.views.add_email")
    return HttpResponseRedirect(request.session.get("next-url", default))

def login (request, out=None):
    if request.GET.get("next", None):
        request.session["next-url"] = request.GET.get("next")

    if request.user.is_authenticated():
        return next(request)
    if out:
        return HttpResponseRedirect(singly.http.connect(out, redirect_uri=request.build_absolute_uri(reverse("sv-bounce"))))

    return render(request, "supervisor/login.html")

def logout (request):
    auth.logout(request)
    return next(request)

def bounce (request):
    """Handles bouncing after a Singly login."""
    code = request.GET.get("code")
    if code is None:
        return next(request)
    data = singly.http.fetch_token(code)

    if data is None:
        return HttpResponse("No result from singly. Authentication failed?")

    # This could probably be put into a separate logic function
    user = auth.login(request, data)
    return next(request)

def add_email (request):
    if not request.user.is_authenticated():
        return next(request)

    form = EmailForm()
    if request.POST:
        form = EmailForm(request.POST)
        if form.is_valid():
            request.user.email = form.cleaned_data.get("email")
            request.user.save()
            return next(request)
    return render(request, "supervisor/add_email.html", {"form" : form})