"""
URL Configuration for "/users/..." and all its children.

Regex expression not split across lines -- pyline warnings supressed
using "# pylint: disable=C0301"

TODO:
1. Source extras
2. Source version for about, details, etc. -- only implemented now for concepts/mappings tabs
"""
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import (patterns, url)

from users.views import (
    UserListView, UserRedirectView, UserDetailView, UserUpdateView)

from apps.sources.views import (
    SourceDetailsView, SourceAboutView, SourceConceptsView, SourceMappingsView,
    SourceNewView, SourceEditView, SourceVersionsView, SourceExternalReferencesView,
    SourceVersionsNewView, SourceVersionsEditView, SourceVersionsRetireView, SourceDeleteView)
from apps.concepts.views import (
    ConceptDetailsView, ConceptMappingsView, ConceptHistoryView, ConceptEditView,
    ConceptRetireView, ConceptNewView, ConceptDescView, ConceptNameView)
from apps.mappings.views import (
    MappingDetailsView, MappingNewView, MappingEditView, MappingRetireView)
from apps.core.views import ExtraJsonView
from apps.collections.views import CollectionDetailView, CollectionCreateView, CollectionEditView, CollectionAboutView, \
    CollectionVersionsView, CollectionConceptsView, CollectionMappingsView, \
    CollectionReferencesView, CollectionDeleteView, CollectionAddReferenceView

urlpatterns = patterns(
    '',


    ## SOURCES CORE

    # /users/:user/sources/new/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/new/$',
        SourceNewView.as_view(), name='source-new'),

    # /users/:user/sources/:source/ - points to "source-details"
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/$',
        SourceDetailsView.as_view(), name='source-home'),

    # /users/:user/sources/:source/details/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/details/$',
        SourceDetailsView.as_view(), name='source-details'),

    # /users/:user/sources/:source/edit/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$',
        SourceEditView.as_view(), name='source-edit'),

    # /users/:user/sources/:source/delete/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/delete/$',
        SourceDeleteView.as_view(), name='source-delete'),

    # /users/:user/sources/:source/about/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/about/$',
        SourceAboutView.as_view(), name='source-about'),

    # /users/:user/sources/:source/concepts/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/$',
        SourceConceptsView.as_view(), name='source-concepts'),

    # /users/:user/sources/:source/:version/concepts/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<source_version>[a-zA-Z0-9\-\.]+)/concepts/$',    # pylint: disable=C0301
        SourceConceptsView.as_view(), name='source-version-concepts'),

    # /users/:user/sources/:source/mappings/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/$',
        SourceMappingsView.as_view(), name='source-mappings'),

    # /users/:user/sources/:source/:version/mappings/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<source_version>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        SourceMappingsView.as_view(), name='source-version-mappings'),

    # /users/:user/sources/:source/extrefs/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extrefs/$',
        SourceExternalReferencesView.as_view(), name='source-extrefs'),

    # /users/:user/sources/:source/versions/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/$',
        SourceVersionsView.as_view(), name='source-versions'),

    # /users/:user/sources/:source/versions/new/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/new/$',
        SourceVersionsNewView.as_view(), name='source-version-new'),

    # /users/:user/sources/:source/versions/edit/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<source_version>[a-zA-Z0-9\-\.]+)/edit/$',    # pylint: disable=C0301
        SourceVersionsEditView.as_view(), name='source-version-edit'),

    # /users/:user/sources/:source/versions/retire/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<source_version>[a-zA-Z0-9\-\.]+)/retire/$',    # pylint: disable=C0301
        SourceVersionsRetireView.as_view(), name='source-version-retire'),



    # /users/:user/sources/:source/extras/ - JSON ONLY - Angular
    #url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/$',
    #    ExtraJsonView.as_view(), name='source-extra'),

    # /users/:user/sources/:source/extras/extra/ - JSON ONLY - Angular
    #url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
    #    ExtraJsonView.as_view(), name='source-extra-add'),



    ## CONCEPTS

    # /users/:user/sources/:source/concepts/new/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/new/$',
        ConceptNewView.as_view(), name='concept-new'),

    # /users/:user/sources/:source/concepts/:concept/ - points to "concept-details"
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-home'),

    # /users/:user/sources/:source/concepts/:concept/:version - points to "concept-details"
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-home-versioned'),

    # /users/:user/sources/:source/concepts/:concept/edit/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/edit/$',    # pylint: disable=C0301
        ConceptEditView.as_view(), name='concept-edit'),

    # /users/:user/sources/:source/concepts/:concept/retire/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/retire/$',    # pylint: disable=C0301
        ConceptRetireView.as_view(), name='concept-edit'),

    # /users/:user/sources/:source/concepts/:concept/details/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/details/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-details'),

    # /users/:user/sources/:source/concepts/:concept/mappings/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingsView.as_view(), name='concept-mappings'),

    # /users/:user/sources/:source/concepts/:concept/history/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/history/$',    # pylint: disable=C0301
        ConceptHistoryView.as_view(), name='concept-history'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/ - points to "concept-version-details"
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-home'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/details/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/details/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-details'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/mappings/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingsView.as_view(), name='concept-version-mappings'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/history/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/history/$',    # pylint: disable=C0301
        ConceptHistoryView.as_view(), name='concept-version-history'),



    ## CONCEPT NAMES - old JSON Angular URLs

    # /users/:user/sources/:source/concepts/:concept/names/ - JSON ANGULAR
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),
    # /users/:user/sources/:source/concepts/:concept/:concept-version/names/ - JSON ANGULAR
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),
    # /users/:user/sources/:source/concepts/:concept/names/:concept-name/ - JSON ANGULAR
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-ud'),

    ## CONCEPT DESCRIPTIONS - old JSON Angular URLs

    # /users/:user/sources/:source/concepts/:concept/descriptions/ - JSON ANGULAR
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /users/:user/sources/:source/concepts/:concept/:concept-version/descriptions/ - JSON ANGULAR
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /users/:user/sources/:source/concepts/:concept/descriptions/:concept-description/ - JSON ANGULAR
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-ud'),

    ## CONCEPT EXTRAS - old JSON Angular URLs

    # /users/:user/sources/:source/concepts/:concept/extras/ - JSON ANGULAR
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /users/:user/sources/:source/concepts/:concept/:concept-version/extras/ - JSON ANGULAR
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /users/:user/sources/:source/concepts/:concept/extras/:extra/ - JSON ANGULAR
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra-add'),



    # PERMALINKS FOR CONCEPT SUB-RESOURCES

    # /users/:user/sources/:source/concepts/:concept/names/:name/ - PERMALINK
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-name'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/names/:name/ - PERMALINK
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-name'),

    # /users/:user/sources/:source/concepts/:concept/descriptions/:description/ - PERMALINK
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-description'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/descriptions/:description/ - PERMALINK
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-description'),



    ## MAPPINGS

    # /users/:user/sources/:source/mappings/new/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/new/$',    # pylint: disable=C0301
        MappingNewView.as_view(), name='mapping-new'),

    # /users/:user/sources/:source/mappings/:mapping/ - points to "mapping-details"
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-home'),

    # /users/:user/sources/:source/mappings/:mapping/details/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/details/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-details'),

    # /users/:user/sources/:source/mappings/:mapping/edit/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/edit/$',    # pylint: disable=C0301
        MappingEditView.as_view(), name='mapping-edit'),

    # /users/:user/sources/:source/mappings/:mapping/retire/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/retire/$',    # pylint: disable=C0301
        MappingRetireView.as_view(), name='mapping-retire'),



    ## CORE USER - are these used at all?

    # URL pattern for the UserListView
    url(r'^$',
        UserListView.as_view(), name='list'),

    # URL pattern for the UserRedirectView
    url(r'^~redirect/$',
        UserRedirectView.as_view(), name='redirect'),

    # URL pattern for the UserDetailView
    url(r'^(?P<username>[\w@\.\+\-_]+)/$',
        UserDetailView.as_view(), name='detail'),

    # URL pattern for the UserUpdateView
    url(r'^update/(?P<username>[\w@\.\+\-_]+)/$',
        UserUpdateView.as_view(), name='update'),



    ## SELFISH URLs
    # NOTE: Placed at the end so that reserved words aren't incorrectly treated like mnemonics

    # /users/:user/sources/:source/:version/ - points to 'source-details'
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<source_version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        SourceDetailsView.as_view(), name='source-version-home'),

    ## Collection CORE

    # /users/:user/collections/new/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/new/$',
        CollectionCreateView.as_view(), name='collection-new'),

    # /users/:user/collections/:collection/details/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/details/$',
        CollectionDetailView.as_view(), name='collection-details'),

    # /users/:user/collections/:collection/ - points to "collection-details"
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/$',
        CollectionDetailView.as_view(), name='collection-home'),
    # /users/:user/collections/:collection/edit/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/edit/$',
        CollectionEditView.as_view(), name='collection-edit'),
    # /users/:user/collections/:collection/about/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/about/$',
        CollectionAboutView.as_view(), name='collection-about'),
    # /users/:user/collections/:collection/versions/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/versions/$',
        CollectionVersionsView.as_view(), name='collection-versions'),
    # /users/:user/collections/:collection/concepts/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/concepts/$',
        CollectionConceptsView.as_view(), name='collection-concepts'),
    # /users/:user/collections/:collection/mappings/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/mappings/$',
        CollectionMappingsView.as_view(), name='collection-mappings'),
    # /users/:user/collections/:collection/references/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/references/$',
        CollectionReferencesView.as_view(), name='collection-references'),
    # /orgs/:org/collections/:collection/delete/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/delete/$',
        CollectionDeleteView.as_view(), name='collection-delete'),
    # /orgs/:org/collections/:collection/addreference/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/collections/(?P<collection>[a-zA-Z0-9\-\.]+)/addreference/$',
        CollectionAddReferenceView.as_view(), name='collection-addreference'),
)
