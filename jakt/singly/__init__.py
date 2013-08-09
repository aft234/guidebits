# coding=utf-8
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

client_id = settings.SINGLY_CLIENT_ID
client_secret = settings.SINGLY_CLIENT_SECRET

if not client_id or not client_secret:
    raise ImproperlyConfigured("Must define SINGLY_CLIENT_ID and SINGLY_CLIENT_SECRET.")