# coding=utf-8
"""Product listing urls."""

from django.conf.urls import patterns, include, url

urlpatterns = patterns("product.views",
    url(r"^all$", "all"),
    url(r"^manage$", "management"),
    url(r"^add$", "add"),
    url(r"^edit/(?P<pk>\d+)$", "edit"),
)
