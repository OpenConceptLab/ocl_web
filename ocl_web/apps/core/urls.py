from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from .views import GetLocalesView

urlpatterns = patterns('',
    url(r'^locales/$', GetLocalesView.as_view(), name='locale-list'),
)
