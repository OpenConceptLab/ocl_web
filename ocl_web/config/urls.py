# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.ocl_search.views import HomeSearchView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    ######### Concepts
    # List

    ######### Sources
    # List

    ######### Orgs
    # List

    ######### Users
    # List

    ######### Search
    url(r'^search/$', HomeSearchView.as_view(), name="search"),
    url(r'^$',
        TemplateView.as_view(template_name='pages/home.html'),
        name="home"),
    url(r'^about/$',
        TemplateView.as_view(template_name='pages/about.html'),
        name="about"),
    url(r'^features/$',
        TemplateView.as_view(template_name='pages/features.html'),
        name="features"),
    url(r'^plans/$',
        TemplateView.as_view(template_name='pages/plans.html'),
        name="plans"),
    url(r'^contact/$',
        TemplateView.as_view(template_name='pages/contact.html'),
        name="contact"),
    url(r'^api/$',
        TemplateView.as_view(template_name='pages/api.html'),
        name="api"),
    url(r'^explore/$',
        TemplateView.as_view(template_name='pages/explore.html'),
        name="explore"),
    url(r'^help/$',
        TemplateView.as_view(template_name='pages/help.html'),
        name="help"),
    url(r'^entity/$',
        TemplateView.as_view(template_name='pages/entity.html'),
        name="entity"),
    url(r'^repo/$',
        TemplateView.as_view(template_name='pages/repo.html'),
        name="repo"),
    url(r'^source/$',
        TemplateView.as_view(template_name='pages/source.html'),
        name="source"),
    url(r'^collection/$',
        TemplateView.as_view(template_name='pages/collection.html'),
        name="collection"),
    url(r'^concept/$',
        TemplateView.as_view(template_name='pages/concept.html'),
        name="concept"),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # User management
    url(r'^users/', include("users.urls", namespace="users")),
    url(r'^accounts/', include('allauth.urls')),

    # Uncomment the next line to enable avatars
    url(r'^avatar/', include('avatar.urls')),

    # Your stuff: custom urls go here

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
