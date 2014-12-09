from django.conf.urls import patterns, url, include
from .views import CollectionDetailView

__author__ = 'briandant'

urlpatterns = patterns('',
#    url(r'^$', CollectionListView.as_view(), name='collection-list'),
    url(r'^(?P<collection>[a-zA-Z0-9\-\.]+)/$', CollectionDetailView.as_view(), name='collection-detail'),
#    url(r'^(?P<collection>[a-zA-Z0-9\-\.]+)/concepts/', include('apps.concepts.urls')),
)
