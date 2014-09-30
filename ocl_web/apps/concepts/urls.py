from django.conf.urls import patterns, url

from apps.concepts.views import (ConceptDetailView, ConceptCreateView, ConceptNamesUpdateView, ConceptNameAddView)


urlpatterns = patterns('',
    url(r'^create/(?P<org>[a-zA-Z0-9\-\.]+)/(?P<source>[a-zA-Z0-9\-\.]+)/$', ConceptCreateView.as_view(), name='concept-create'),
#    url(r'^detail/(?P<org>[a-zA-Z0-9\-\.]+)/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<concept>[a-zA-Z0-9\-\.]+)/$', ConceptDetailView.as_view(), name='concept-detail'),
    url(r'^detail/(?P<org>[a-zA-Z0-9\-\.]+)/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<concept>[a-zA-Z0-9\-\.]+)/$', ConceptNameAddView.as_view(), name='concept-detail'),
    url(r'^update/names/(?P<org>[a-zA-Z0-9\-\.]+)/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<concept>[a-zA-Z0-9\-\.]+)/$', ConceptNamesUpdateView.as_view(), name='concept-names-update'),
    url(r'^detail/(?P<org>[a-zA-Z0-9\-\.]+)/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<concept>[a-zA-Z0-9\-\.]+)/name/add/$', ConceptNameAddView.as_view(), name='concept-name-add'),

#    url(r'^(?P<concept>[a-zA-Z0-9\-\.]+)/versions/$', ConceptVersionsView.as_view(), name='concept-version-list'),
#    url(r'^(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/$', ConceptVersionRetrieveView.as_view(), name='conceptversion-detail'),
)
