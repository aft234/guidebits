# coding=utf-8
import logging
logger = logging.getLogger(__name__)

from functools import wraps

# Django stuff
from django.core.urlresolvers import resolve, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import available_attrs
from django.core.exceptions import PermissionDenied

# Project specific
from utility import annoying as a

def simple_shim (d, f=None):
    if callable(f):
        return d(f)
    return d

def decorator_shim (d, f, *a, **k):
    """Quick shim for the if func: return logic."""
    b = d(*a, **k)
    return simple_shim(b, f)

def requires_login (func=None):
    def decorator (view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view (request, *args, **kwargs):
            if request.user.is_authenticated() is False:
                return HttpResponseRedirect("{0}?next={1}".format(reverse("sv-login"), request.path))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return simple_shim(decorator, func)

def requires_staff (func=None):
    def decorator (view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view (request, *args, **kwargs):
            if not request.user.is_authenticated() or not request.user.is_staff:
                return HttpResponseRedirect("{0}?next={1}".format(reverse("sv-login"), request.path))
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return simple_shim(decorator, func)
