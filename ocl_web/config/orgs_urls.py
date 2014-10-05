# -*- coding: utf-8 -*-
"""
    urls under "orgs"
"""

from __future__ import unicode_literals

from django.conf.urls import (patterns, url)
from django.conf.urls.static import static
from django.views.generic import TemplateView

from apps.orgs.views import (OrganizationDetailView, OrganizationCreateView, OrganizationEditView)
from apps.sources.views import (SourceDetailView, SourceCreateView, SourceEditView)
from apps.concepts.views import (ConceptDetailView, ConceptCreateView, ConceptEditView)
from apps.concepts.views import (ConceptNamesUpdateView, ConceptNameAddView)
from apps.concepts.views import (ConceptDescView, ConceptNameView)

urlpatterns = patterns('',

    url(r'^create/$', OrganizationCreateView.as_view(), name='org-create'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/$', OrganizationDetailView.as_view(), name='org-detail'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/edit/$', OrganizationEditView.as_view(), name='org-edit'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/$', SourceDetailView.as_view(), name='source-detail'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/$', SourceCreateView.as_view(), name='source-create-for-org'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$', SourceEditView.as_view(), name='source-edit'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/create/$', ConceptCreateView.as_view(), name='concept-create-for-org'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/$', ConceptNameAddView.as_view(), name='concept-detail'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/edit/$', ConceptEditView.as_view(), name='concept-edit'),

    url(r'^update/names/(?P<org>[a-zA-Z0-9\-\.]+)/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<concept>[a-zA-Z0-9\-\.]+)/$', ConceptNamesUpdateView.as_view(), name='concept-names-update'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/add/$', ConceptNameAddView.as_view(), name='concept-name-add'),

    # name views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/$', ConceptNameView.as_view(), name='concept-name'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$', ConceptNameView.as_view(), name='concept-desc-add'),

    # desc views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/$', ConceptDescView.as_view(), name='concept-desc'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$', ConceptDescView.as_view(), name='concept-desc-add'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collection/(?P<collection>[a-zA-Z0-9\-\.]+)/$', ConceptNameAddView.as_view(), name='collection-detail'),
)
