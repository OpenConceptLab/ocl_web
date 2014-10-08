# -*- coding: utf-8 -*-
"""
    urls under "orgs"
"""

from __future__ import unicode_literals

from django.conf.urls import (patterns, url)

from apps.orgs.views import (OrganizationDetailView, OrganizationCreateView, OrganizationEditView)
from apps.sources.views import (SourceDetailView, SourceCreateView, SourceEditView)
from apps.sources.views import (SourceVersionView)
from apps.concepts.views import (ConceptDetailView, ConceptCreateView, ConceptEditView)
from apps.concepts.views import (ConceptDescView, ConceptNameView, ConceptVersionListView, ConceptExtraView)
from apps.core.views import ExtraJsonView

urlpatterns = patterns('',

    url(r'^create/$', OrganizationCreateView.as_view(), name='org-create'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/$', OrganizationDetailView.as_view(), name='org-detail'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/edit/$', OrganizationEditView.as_view(), name='org-edit'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/$', SourceDetailView.as_view(), name='source-detail'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/$', SourceCreateView.as_view(), name='source-create-for-org'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$', SourceEditView.as_view(), name='source-edit'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/$', SourceVersionView.as_view(), name='source-version-cl'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/(?P<version>[a-zA-Z0-9\-\.]+)/$', SourceVersionView.as_view(), name='source-version-ud'),

    # source extra views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/$', ExtraJsonView.as_view(), name='source-extra'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$', ExtraJsonView.as_view(), name='source-extra-add'),


    # concept views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/create/$', ConceptCreateView.as_view(), name='concept-create-for-org'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/$', ConceptDetailView.as_view(), name='concept-detail'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/edit/$', ConceptEditView.as_view(), name='concept-edit'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/versions/$', ConceptVersionListView.as_view(), name='concept-version-list'),

    # concept name views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/$', ConceptNameView.as_view(), name='concept-name-cl'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$', ConceptNameView.as_view(), name='concept-name-ud'),

    # concept desc views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/$', ConceptDescView.as_view(), name='concept-desc-cl'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$', ConceptDescView.as_view(), name='concept-desc-ud'),

    # concept extra views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/$', ConceptExtraView.as_view(), name='concept-extra'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$', ConceptExtraView.as_view(), name='concept-extra-add'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collection/(?P<collection>[a-zA-Z0-9\-\.]+)/$', ConceptDetailView.as_view(), name='collection-detail'),
)
