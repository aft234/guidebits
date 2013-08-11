# coding=utf-8
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

client_id = settings.SINGLY_CLIENT_ID
client_secret = settings.SINGLY_CLIENT_SECRET
api_url = settings.SINGLY_URL

twitter_key = settings.TWITTER_KEY
twitter_secret = settings.TWITTER_SECRET

if not client_id or not client_secret or not api_url:
    raise ImproperlyConfigured("Must define: SINGLY_CLIENT_ID={0}, SINGLY_CLIENT_SECRET={1}, and SINGLY_URL={2}.".format(client_id, client_secret, api_url))