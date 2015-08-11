# -*- coding: utf-8 -*-
"""
Core URLs -- this URL config file is active! Although, not using these pages.
"""
from django.conf.urls import patterns, url

from .views import (GetOptionListView, GetStatsView)

urlpatterns = patterns(
    '',
    url(r'^options/(?P<type>[a-z\-_]+)/$', GetOptionListView.as_view(), name='option-list'),
    url(r'^stats/(?P<key>[a-z\-_]+)/$', GetStatsView.as_view(), name='core-stats')
)
