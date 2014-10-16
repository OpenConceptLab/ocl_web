from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from .views import GetOptionListView

urlpatterns = patterns('',
    url(r'^options/(?P<type>[a-z\-_]+)/$', GetOptionListView.as_view(), name='option-list'),
)
