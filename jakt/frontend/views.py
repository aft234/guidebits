# coding=utf-8
"""Frontend views"""

import logging, os
logger = logging.getLogger(__name__)

# Django imports
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from product import views as pviews
def home (request):
    return pviews.all(request)
    # return render(request, "frontend/home.html")

def about (request):
    return render(request, "frontend/about.html", {"current": "about"})

def hiw (request):
    return render(request, "frontend/hiw.html", {"current": "hiw"})

def contact (request):
    return render(request, "frontend/contact.html", {"current": "contact"})

def privacy (request):
    return render(request, "frontend/privacy.html")

def tos (request):
    return render(request, "frontend/tos.html")

def internal_error (request):
    return render(request, "frontend/internal_error.html")

def missing_error (request):
    return render(request, "frontend/missing_error.html")

def forbidden_error (request):
    return render(request, "frontend/forbidden_error.html")