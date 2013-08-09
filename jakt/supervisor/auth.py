# coding=utf-8
"""Authentication logic."""

import logging
logger = logging.getLogger(__name__)

# Django imports
from django.contrib.auth import authenticate as dj_authenticate, login as dj_login, logout as dj_logout
from django.conf import settings

# Project imports
from utility import annoying as a
from singly import combined
from singly import http

# Internal imports
from .models import User

def login (request, data):
    singly_id = a.tree_get(data, "account")
    singly_token = a.tree_get(data, "access_token")

    if not singly_id or not singly_token:
        logger.error("Unable to connect user, result from singly: {res}".format(res=data))
    else:
        # Try and find the user associated with this account
        user = a.get_or_none(User, singly_id=singly_id)
        if user is None:

            if not settings.ALLOW_SIGNUP:
                logger.error("Bypassing signup")
                return None

            # Create new user
            logger.debug("Creating new user for {singly_id}".format(singly_id=singly_id))

            # First pull the profile
            profile = combined.get_profile(singly_token)
            username = a.tree_get(profile, "id", lambda d: d[0:30])
            email = a.tree_get(profile, "email")
            first_name, last_name = a.tree_get(profile, "name", lambda n: n.split(" ", 1))

            # Now let's check to see if the email address exists
            user = a.get_or_none(User, email=email)
            if not user:
                # Guess we have to create a new account
                user = User()

                user.first_name = first_name
                user.last_name = last_name
                user.singly_id = singly_id
                user.singly_token = singly_token
                user.username = username
                user.email = email
                if not user.email:
                    user.email = "blank@twitterlogin.com"
                user.save()
            else:
                if not combined.merge(singly_token, user.singly_token):
                    return None

        user.backend = "django.contrib.auth.backends.ModelBackend"
        dj_login(request, user)
        return user

def login_path (user):
    return "index"

def logout (request):
    dj_logout(request)