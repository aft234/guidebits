# coding=utf-8
"""Product listing urls."""

from django.conf.urls import patterns, include, url

urlpatterns = patterns("product.views",
    url(r"^all$", "all"),
    url(r"^(?P<pk>\d+)$", "view_product"),
    url(r"^(?P<pk>\d+)/tweets$", "view_tweets"),
    url(r"^manage$", "management"),
    url(r"^add$", "add"),
    url(r"^edit/(?P<pk>\d+)$", "edit"),
    url(r"^search/(?P<pk>\d+)$", "searches"),
    url(r"^search/(?P<pk>\d+)/add$", "add_search"),
    url(r"^search/(?P<pk>\d+)/view$", "view_search"),
    url(r"^search/(?P<pk>\d+)/delete$", "delete_search"),
)
