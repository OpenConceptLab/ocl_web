from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import (GetOptionListView, GetStatsView)

urlpatterns = patterns('',
    url(r'^options/(?P<type>[a-z\-_]+)/$', GetOptionListView.as_view(), name='option-list'),
    url(r'^stats/(?P<key>[a-z\-_]+)/$', GetStatsView.as_view(), name='core-stats'),
)
