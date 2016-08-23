# -*- coding: utf-8 -*-
"""
Root URL coniguration file as per settings.py.

This file along with orgs_urls.py and users_urls.py are the primary
(or the only?) URL configuration files for OCL.
"""

from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.ocl_search.views import GlobalSearchView
from apps.tests.views import TestTagsView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',

    # OCL Global Search - /search/
    url(r'^search/$', GlobalSearchView.as_view(), name="search"),

    # Organizations - /orgs/...
    url(r'^orgs/', include('config.orgs_urls')),

    # Users - /users/...
    url(r'^users/', include('config.users_urls')),

    # Core - /core/options/datatypes/ OR /core/stats/concepts/
    # TODO(paynejd@gmail.com): Core stats/options is interesting but needs to be thought through
    url(r'^core/', include('apps.core.urls')),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # User avatars - /avatar/...
    url(r'^avatar/', include('avatar.urls')),

    # Testing
    url(r'^tests/tags/$', TestTagsView.as_view(), name="test-tags"),

    # Static pages (some to be moved into Dynamic views later)
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name="home"),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name="about"),
    url(r'^features/$', TemplateView.as_view(template_name='pages/features.html'), name="features"),
    url(r'^plans/$', TemplateView.as_view(template_name='pages/plans.html'), name="plans"),
    url(r'^contact/$', TemplateView.as_view(template_name='pages/contact.html'), name="contact"),
    url(r'^api/$', TemplateView.as_view(template_name='pages/api.html'), name="api"),
    url(r'^explore/$', TemplateView.as_view(template_name='pages/explore.html'), name="explore"),
    url(r'^terms/$', TemplateView.as_view(template_name='pages/terms.html'), name="terms"),
    url(r'^privacy/$', TemplateView.as_view(template_name='pages/privacy.html'), name="privacy"),
    url(r'^license/$', TemplateView.as_view(template_name='pages/license.html'), name="license"),
    url(r'^help/$', TemplateView.as_view(template_name='pages/help.html'), name="help"),

    # TODO(paynejd@gmail.com): Temporary success page -- remove?
    #url(r'^success/$', TemplateView.as_view(template_name='pages/success.html'),
    #    name="form-success"),

    # Admin - /admin/...
    url(r'^admin/', include(admin.site.urls)),


) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
