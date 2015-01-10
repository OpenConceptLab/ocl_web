# -*- coding: utf-8 -*-
"""
    urls under "orgs"
"""

from __future__ import unicode_literals

from django.conf.urls import (patterns, url)

from apps.orgs.views import (OrganizationDetailView, OrganizationCreateView, OrganizationEditView)
from apps.sources.views import (SourceDetailView, SourceCreateView, SourceEditView)
from apps.sources.views import (SourceVersionView)
from apps.collections.views import (CollectionDetailView, CollectionCreateView, CollectionEditView)
from apps.concepts.views import (ConceptDetailView, ConceptEditView, ConceptCreateJsonView)
from apps.concepts.views import (ConceptDescView, ConceptNameView, ConceptVersionListView, ConceptMappingView)
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


    # collections
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/$', CollectionDetailView.as_view(), name='collection-detail'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/$', CollectionCreateView.as_view(), name='collection-create-for-org'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$', SourceEditView.as_view(), name='collection-edit'),

    # concept views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/create/$', ConceptCreateJsonView.as_view(), name='concept-create-for-org'),

    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/$', ConceptDetailView.as_view(), name='concept-detail'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/edit/$', ConceptCreateJsonView.as_view(), name='concept-edit'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/versions/$', ConceptVersionListView.as_view(), name='concept-version-list'),

    # concept name views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/$', ConceptNameView.as_view(), name='concept-name-cl'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$', ConceptNameView.as_view(), name='concept-name-ud'),

    # concept desc views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/$', ConceptDescView.as_view(), name='concept-desc-cl'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$', ConceptDescView.as_view(), name='concept-desc-ud'),

    # concept mappin views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/$', ConceptMappingView.as_view(), name='concept-mapping-cl'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$', ConceptMappingView.as_view(), name='concept-mapping-ud'),

    # concept extra views
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/$', ExtraJsonView.as_view(), name='concept-extra'),
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$', ExtraJsonView.as_view(), name='concept-extra-add'),

)
