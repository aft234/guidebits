# coding=utf-8
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import handler500, handler404, handler403
from django.contrib import admin
admin.autodiscover()

# Setup error handlers
handler500 = "frontend.views.internal_error"
handler404 = "frontend.views.missing_error"
handler403 = "frontend.views.forbidden_error"

urlpatterns = patterns('',
    # Routes
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/',  include('supervisor.urls')),
    url(r'^games/', include('product.urls')),
    url(r'^',       include('frontend.urls')),
)
