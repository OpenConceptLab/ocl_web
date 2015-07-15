# -*- coding: utf-8 -*-
"""
URL Configuration for "/orgs/..." and all its children.

Regex expression not split across lines -- pyline warnings supressed using "# pylint: disable=C0301"
"""

from __future__ import unicode_literals

from django.conf.urls import (patterns, url)
from apps.orgs.views import (
    OrganizationDetailsView, OrganizationAboutView, OrganizationSourcesView,
    OrganizationNewView, OrganizationEditView,
    OrganizationMemberAddView, OrganizationMemberRemoveView)
from apps.sources.views import (
    SourceDetailsView, SourceAboutView, SourceConceptsView, SourceMappingsView,
    SourceDetailView, SourceCreateView, SourceEditView, SourceVersionView, SourceVersionsView)
from apps.mappings.views import (MappingDetailsView)
from apps.concepts.views import (
    ConceptDetailView, ConceptCreateJsonView, ConceptRetireView,
    ConceptDescView, ConceptNameView, ConceptVersionListView, ConceptMappingView)
from apps.core.views import ExtraJsonView
#from apps.collections.views import (
#    CollectionDetailView, CollectionCreateView, CollectionEditView)


urlpatterns = patterns(
    '',

    ## ORGANIZATION

    # Create new organization - /orgs/new/
    url(r'^new/$', OrganizationNewView.as_view(), name='org-new'),

    # /orgs/:org/
    # TODO(paynejd@gmail.com): Potentially point /orgs/:org/ to org sources instead of details
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/$',
        OrganizationDetailsView.as_view()),

    # /orgs/:org/edit/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/edit/$',
        OrganizationEditView.as_view(), name='org-edit'),

    # /orgs/:org/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/details/$',
        OrganizationDetailsView.as_view(), name='org-details'),

    # /orgs/:org/about/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/about/$',
        OrganizationAboutView.as_view(), name='org-about'),

    # /orgs/:org/sources/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/$',
        OrganizationSourcesView.as_view(), name='org-sources'),

    # /orgs/:org/collections/
    # TODO(paynejd@gmail.com): Activate /orgs/:org/collections/ after implemented
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/$',
    #    OrganizationCollectionsView.as_view(), name='org-collections'),


    ## ORGANIZATION MEMBERS

    # /orgs/:org/members/add/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/add/$',
        OrganizationMemberAddView.as_view(), name='org-member-add'),

    # /orgs/:org/members/remove/:username/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/remove/(?P<username>[a-zA-Z0-9\-\.]+)/$',
        OrganizationMemberRemoveView.as_view(), name='org-member-remove'),


    ## SOURCES CORE

    # /orgs/:org/sources/new/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/new/$',
        SourceCreateView.as_view(), name='source-create-for-org'),

    # /orgs/:org/sources/:source/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/$',
        SourceDetailView.as_view(), name='source-detail'),

    # /orgs/:org/sources/:source/edit/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$',
        SourceEditView.as_view(), name='source-edit'),

    # /orgs/:org/sources/:source/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/details/$',
        SourceDetailsView.as_view(), name='source-details'),

    # /orgs/:org/sources/:source/about/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/about/$',
        SourceAboutView.as_view(), name='source-about'),

    # /orgs/:org/sources/:source/concepts/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/$',
        SourceConceptsView.as_view(), name='source-concepts'),

    # /orgs/:org/sources/:source/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/$',
        SourceMappingsView.as_view(), name='source-mappings'),

    # /orgs/:org/sources/:source/versions/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/$',
        SourceVersionsView.as_view(), name='source-versions'),


    # /orgs/:org/sources/:source/versions/ - JSON ONLY - Angular
    # TODO(paynejd@gmail.com): Overwritten and probably means creating/editing/viewing source versions will fail with angular
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/$',
    #    SourceVersionView.as_view(), name='source-version-cl'),

    # /orgs/:org/sources/:source/versions/:source-version/ - JSON ONLY - Angular
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/(?P<version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        SourceVersionView.as_view(), name='source-version-ud'),

    # /orgs/:org/sources/:source/extras/ - JSON ONLY - Angular
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/$',
        ExtraJsonView.as_view(), name='source-extra'),

    # /orgs/:org/sources/:source/extras/:extra/ - JSON ONLY - Angular
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='source-extra-add'),


    ## COLLECTIONS

    # TODO(paynejd@gmail.com): collections URLs
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/$',
    #    CollectionDetailView.as_view(), name='collection-detail'),
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/$',
    #    CollectionCreateView.as_view(), name='collection-create-for-org'),
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$',
    #    SourceEditView.as_view(), name='collection-edit'),


    ## CONCEPTS

    # New concept: /orgs/:org/sources/:source/create/
    # TODO(paynejd@gmail.com): Change this to: /orgs/:org/sources/:source/concept/new/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/create/$',
        ConceptCreateJsonView.as_view(), name='concept-create-for-org'),

    # /orgs/:org/sources/:source/concepts/:concept/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailView.as_view(), name='concept-detail'),

    # /orgs/:org/sources/:source/concepts/:concept/edit/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/edit/$',    # pylint: disable=C0301
        ConceptCreateJsonView.as_view(), name='concept-edit'),

    # /orgs/:org/sources/:source/concepts/:concept/retire/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/retire/$',    # pylint: disable=C0301
        ConceptRetireView.as_view(), name='concept-retire'),

    # /orgs/:org/sources/:source/concepts/:concept/versions/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/versions/$',    # pylint: disable=C0301
        ConceptVersionListView.as_view(), name='concept-version-list'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/versions/
    # TODO(paynejd@gmail.com): This looks screwy
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/versions/$',    # pylint: disable=C0301
        ConceptVersionListView.as_view(), name='concept-version-list'),


    ## CONCEPT NAMES

    # /orgs/:org/sources/:source/concepts/:concept/names/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/names/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),

    # /orgs/:org/sources/:source/concepts/:concept/names/:concept-name/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-ud'),


    ## CONCEPT DESCRIPTIONS

    # /orgs/:org/sources/:source/concepts/:concept/descriptions/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/descriptions/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/descriptions/:description/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-ud'),


    ## MAPPINGS

    # /orgs/:org/sources/:source/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-details'),

    # TODO(paynejd@gmail.com): Below Mapping URLs are not implemented correctly

    # /orgs/:org/sources/:source/concepts/:concept/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingView.as_view(), name='concept-mapping-cl'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingView.as_view(), name='concept-mapping-cl'),

    # /orgs/:org/sources/:source/concepts/:concept/mappings/:mapping/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptMappingView.as_view(), name='concept-mapping-ud'),

    # /orgs/:org/sources/:source/mappings/:mapping/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptMappingView.as_view(), name='mapping-ud'),


    ## CONCEPT EXTRAS

    # /orgs/:org/sources/:source/concepts/:concept/extras/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/extras/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /orgs/:org/sources/:source/concepts/:concept/extras/:extra/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra-add'),


    # IMPORTANT: we have to move this to the end because the version value
    # can be misinterpreted as /names/ /descriptions/ etc et. Not great URL design
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailView.as_view(), name='concept-detail'),
)
