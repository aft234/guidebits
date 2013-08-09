# coding=utf-8
"""Auth and user management patterns."""

from django.conf.urls import patterns, include, url

urlpatterns = patterns("supervisor.views",
    url(r"^signup/?$", "signup", name="sv-signup"),
    url(r"^login/?$", "login", name="sv-login"),
    url(r"^logout/?$", "logout", name="sv-logout"),
)