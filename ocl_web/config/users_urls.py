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
from libs.ocl import OclConstants

from users.views import (
    UserListView, UserRedirectView, UserDetailView, UserUpdateView, UserJsonView, UserSourcesView, UserCollectionsView)

from apps.sources.views import (
    SourceDetailsView, SourceAboutView, SourceConceptsView, SourceMappingsView,
    SourceNewView, SourceEditView, SourceVersionsView, SourceExternalReferencesView,
    SourceVersionsNewView, SourceVersionsEditView, SourceVersionsRetireView, SourceDeleteView, SourceVersionDeleteView, SourceVersionEditJsonView)
from apps.concepts.views import (
    ConceptDetailsView, ConceptMappingsView, ConceptHistoryView, ConceptEditView,
    ConceptRetireView, ConceptNewView, ConceptDescView, ConceptNameView)
from apps.mappings.views import (
    MappingDetailsView, MappingNewView, MappingEditView, MappingRetireView, MappingVersionsView)
from apps.core.views import ExtraJsonView
from apps.collections.views import CollectionDetailView, CollectionCreateView, CollectionEditView, CollectionAboutView, \
    CollectionVersionsView, CollectionConceptsView, CollectionMappingsView, \
    CollectionReferencesView, CollectionVersionDeleteView, CollectionDeleteView, CollectionAddReferenceView, CollectionVersionsNewView, CollectionReferencesDeleteView, CollectionVersionEditJsonView, \
    CollectionVersionEditView

urlpatterns = patterns(
    '',

    url(r'^$', UserJsonView.as_view(), name='users-json-view'),

    # /users/:user/sources/"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/$',
        UserSourcesView.as_view(), name='user-sources'),

    # /users/:user/collections/"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/$',
        UserCollectionsView.as_view(), name='user-collections'),


    ## SOURCES CORE

    # /users/:user/sources/new/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/new/$',
        SourceNewView.as_view(), name='source-new'),

    # /users/:user/sources/:source/ - points to "source-details"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/$',
        SourceDetailsView.as_view(), name='source-home'),

    # /users/:user/sources/:source/details/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/details/$',
        SourceDetailsView.as_view(), name='source-details'),

    # /users/:user/sources/:source/edit/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/edit/$',
        SourceEditView.as_view(), name='source-edit'),

    # /users/:user/sources/:source/delete/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/delete/$',
        SourceDeleteView.as_view(), name='source-delete'),

    # /users/:user/sources/:source/:version/delete/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<source_version>' + OclConstants.NAMESPACE_PATTERN + ')/delete/$',
        SourceVersionDeleteView.as_view(), name='collection-version-delete'),

    # /users/:user/sources/:source/about/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/about/$',
        SourceAboutView.as_view(), name='source-about'),

    # /users/:user/sources/:source/concepts/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/$',
        SourceConceptsView.as_view(), name='source-concepts'),

    # /users/:user/sources/:source/:version/concepts/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<source_version>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/$',    # pylint: disable=C0301
        SourceConceptsView.as_view(), name='source-version-concepts'),

    # /users/:user/sources/:source/mappings/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/$',
        SourceMappingsView.as_view(), name='source-mappings'),

    # /users/:user/sources/:source/:version/mappings/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<source_version>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/$',    # pylint: disable=C0301
        SourceMappingsView.as_view(), name='source-version-mappings'),

    # /users/:user/sources/:source/extrefs/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/extrefs/$',
        SourceExternalReferencesView.as_view(), name='source-extrefs'),

    # /users/:user/sources/:source/versions/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/versions/$',
        SourceVersionsView.as_view(), name='source-versions'),

    # /users/:user/sources/:source/versions/new/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/versions/new/$',
        SourceVersionsNewView.as_view(), name='source-version-new'),

    # /users/:user/sources/:source/versions/edit/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<source_version>' + OclConstants.NAMESPACE_PATTERN + ')/edit/$',    # pylint: disable=C0301
        SourceVersionsEditView.as_view(), name='source-version-edit'),

    # /users/:user/sources/:source/versions/json/edit/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<source_version>' + OclConstants.NAMESPACE_PATTERN + ')/json/edit/$',    # pylint: disable=C0301
        SourceVersionEditJsonView.as_view(), name='source-version-json-edit'),

    # /users/:user/sources/:source/versions/retire/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<source_version>' + OclConstants.NAMESPACE_PATTERN + ')/retire/$',    # pylint: disable=C0301
        SourceVersionsRetireView.as_view(), name='source-version-retire'),



    # /users/:user/sources/:source/extras/ - JSON ONLY - Angular
    #url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/extras/$',
    #    ExtraJsonView.as_view(), name='source-extra'),

    # /users/:user/sources/:source/extras/extra/ - JSON ONLY - Angular
    #url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/extras/(?P<extra>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
    #    ExtraJsonView.as_view(), name='source-extra-add'),



    ## CONCEPTS

    # /users/:user/sources/:source/concepts/new/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/new/$',
        ConceptNewView.as_view(), name='concept-new'),

    # /users/:user/sources/:source/concepts/:concept/ - points to "concept-details"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-home'),

    # /users/:user/sources/:source/concepts/:concept/:version - points to "concept-details"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/(?P<concept_version>' + OclConstants.NAMESPACE_PATTERN + ')$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-home-versioned'),

    # /users/:user/sources/:source/concepts/:concept/edit/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/edit/$',    # pylint: disable=C0301
        ConceptEditView.as_view(), name='concept-edit'),

    # /users/:user/sources/:source/concepts/:concept/retire/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/retire/$',    # pylint: disable=C0301
        ConceptRetireView.as_view(), name='concept-retire'),

    # /users/:user/sources/:source/concepts/:concept/details/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/details/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-details'),

    # /users/:user/sources/:source/concepts/:concept/mappings/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/mappings/$',    # pylint: disable=C0301
        ConceptMappingsView.as_view(), name='concept-mappings'),

    # /users/:user/sources/:source/concepts/:concept/history/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/history/$',    # pylint: disable=C0301
        ConceptHistoryView.as_view(), name='concept-history'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/ - points to "concept-version-details"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/(?P<concept_version>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-home'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/details/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/(?P<concept_version>' + OclConstants.NAMESPACE_PATTERN + ')/details/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-details'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/mappings/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/(?P<concept_version>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/$',    # pylint: disable=C0301
        ConceptMappingsView.as_view(), name='concept-version-mappings'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/history/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/(?P<concept_version>' + OclConstants.NAMESPACE_PATTERN + ')/history/$',    # pylint: disable=C0301
        ConceptHistoryView.as_view(), name='concept-version-history'),



    ## CONCEPT NAMES - old JSON Angular URLs

    # /users/:user/sources/:source/concepts/:concept/names/ - JSON ANGULAR
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),
    # /users/:user/sources/:source/concepts/:concept/:concept-version/names/ - JSON ANGULAR
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/(?P<concept_version>' + OclConstants.NAMESPACE_PATTERN + ')/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),
    # /users/:user/sources/:source/concepts/:concept/names/:concept-name/ - JSON ANGULAR
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/names/(?P<name>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-ud'),

    ## CONCEPT DESCRIPTIONS - old JSON Angular URLs

    # /users/:user/sources/:source/concepts/:concept/descriptions/ - JSON ANGULAR
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /users/:user/sources/:source/concepts/:concept/:concept-version/descriptions/ - JSON ANGULAR
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/(?P<concept_version>' + OclConstants.NAMESPACE_PATTERN + ')/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /users/:user/sources/:source/concepts/:concept/descriptions/:concept-description/ - JSON ANGULAR
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/descriptions/(?P<description>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-ud'),

    ## CONCEPT EXTRAS - old JSON Angular URLs

    # /users/:user/sources/:source/concepts/:concept/extras/ - JSON ANGULAR
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /users/:user/sources/:source/concepts/:concept/:concept-version/extras/ - JSON ANGULAR
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/(?P<concept_version>' + OclConstants.NAMESPACE_PATTERN + ')/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /users/:user/sources/:source/concepts/:concept/extras/:extra/ - JSON ANGULAR
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/extras/(?P<extra>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra-add'),



    # PERMALINKS FOR CONCEPT SUB-RESOURCES

    # /users/:user/sources/:source/concepts/:concept/names/:name/ - PERMALINK
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/names/(?P<name>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-name'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/names/:name/ - PERMALINK
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/names/(?P<name>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-name'),

    # /users/:user/sources/:source/concepts/:concept/descriptions/:description/ - PERMALINK
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/descriptions/(?P<description>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-description'),

    # /users/:user/sources/:source/concepts/:concept/:concept-version/descriptions/:description/ - PERMALINK
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/(?P<concept>' + OclConstants.CONCEPT_ID_PATTERN + ')/descriptions/(?P<description>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-description'),



    ## MAPPINGS

    # /users/:user/sources/:source/mappings/new/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/new/$',    # pylint: disable=C0301
        MappingNewView.as_view(), name='mapping-new'),

    # /users/:user/sources/:source/mappings/:mapping/ - points to "mapping-details"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/(?P<mapping>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-home'),

    # /users/:user/sources/:source/mappings/:mapping/details/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/(?P<mapping>' + OclConstants.NAMESPACE_PATTERN + ')/details/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-details'),

    # /users/:user/sources/:source/mappings/:mapping/ - points to "mapping-details"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/(?P<mapping>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<mapping_version>' + OclConstants.NAMESPACE_PATTERN + ')/details/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-details'),

    # /users/:user/sources/:source/mappings/:mapping/history/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/(?P<mapping>' + OclConstants.NAMESPACE_PATTERN + ')/history/$',    # pylint: disable=C0301
        MappingVersionsView.as_view(), name='mapping-versions'),

    # /users/:user/sources/:source/mappings/:mapping/edit/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/(?P<mapping>' + OclConstants.NAMESPACE_PATTERN + ')/edit/$',    # pylint: disable=C0301
        MappingEditView.as_view(), name='mapping-edit'),

    # /users/:user/sources/:source/mappings/:mapping/retire/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/(?P<mapping>' + OclConstants.NAMESPACE_PATTERN + ')/retire/$',    # pylint: disable=C0301
        MappingRetireView.as_view(), name='mapping-retire'),

    # /users/:user/sources/:source/mappings/:mapping/ - points to "mapping-details"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/(?P<mapping>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<mapping_version>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-version-home'),

    # /users/:user/sources/:source/mappings/:mapping/ - points to "mapping-details"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/(?P<mapping>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<mapping_version>' + OclConstants.NAMESPACE_PATTERN + ')/history/$',    # pylint: disable=C0301
        MappingVersionsView.as_view(), name='mapping-versions'),


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
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/sources/(?P<source>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<source_version>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        SourceDetailsView.as_view(), name='source-version-home'),

    ## Collection CORE

    # /users/:user/collections/new/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/new/$',
        CollectionCreateView.as_view(), name='collection-new'),

    # /users/:user/collections/:collection/details/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/details/$',
        CollectionDetailView.as_view(), name='collection-details'),

    # /users/:user/collections/:collection/ - points to "collection-details"
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/$',
        CollectionDetailView.as_view(), name='collection-home'),
    # /users/:user/collections/:collection/edit/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/edit/$',
        CollectionEditView.as_view(), name='collection-edit'),
    # /users/:user/collections/:collection/about/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/about/$',
        CollectionAboutView.as_view(), name='collection-about'),
    # /users/:user/collections/:collection/versions/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/versions/$',
        CollectionVersionsView.as_view(), name='collection-versions'),
    # /users/:user/collections/:collection/:collection_version/edit/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<collection_version>' + OclConstants.NAMESPACE_PATTERN + ')/edit/$',
        CollectionVersionEditView.as_view(), name='collection-version-edit'),
    # /users/:user/collections/:collection/:collection_version/json/edit/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<collection_version>' + OclConstants.NAMESPACE_PATTERN + ')/json/edit/$',
        CollectionVersionEditJsonView.as_view(), name='collection-version-json-edit'),
    # /users/:user/collections/:collection/concepts/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/$',
        CollectionConceptsView.as_view(), name='collection-concepts'),
    # /users/:user/collections/:collection/:collection_version/concepts/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<collection_version>' + OclConstants.NAMESPACE_PATTERN + ')/concepts/$',
        CollectionConceptsView.as_view(), name='collection-version-concepts'),
    # /users/:user/collections/:collection/mappings/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/$',
        CollectionMappingsView.as_view(), name='collection-mappings'),
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<collection_version>' + OclConstants.NAMESPACE_PATTERN + ')/mappings/$',
        CollectionMappingsView.as_view(), name='collection-mappings'),
    # /users/:user/collections/:collection/references/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/references/$',
        CollectionReferencesView.as_view(), name='collection-references'),
    # /users/:user/collections/:collection/references/delete
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/references/delete/$',
        CollectionReferencesDeleteView.as_view(), name='collection-references-delete'),
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<collection_version>' + OclConstants.NAMESPACE_PATTERN + ')/references/$',
        CollectionReferencesView.as_view(), name='collection-version-references'),

    # /user/:user/collections/:collection/:collection_version/delete/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<collection_version>' + OclConstants.NAMESPACE_PATTERN + ')/delete/$',
        CollectionVersionDeleteView.as_view(), name='collection-version-delete'),
    # /user/:user/collections/:collection/delete/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/delete/$',
        CollectionDeleteView.as_view(), name='collection-delete'),

    # /orgs/:org/collections/:collection/addreference/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/references/new/$',
        CollectionAddReferenceView.as_view(), name='collection-addreference'),

    # /users/:user/collections/:collection/versions/new/
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/versions/new/$',
        CollectionVersionsNewView.as_view(), name='collection-version-new'),
    # /users/:user/collections/:collection/:version/ - points to 'collection-details'
    url(r'^(?P<user>' + OclConstants.NAMESPACE_PATTERN + ')/collections/(?P<collection>' + OclConstants.NAMESPACE_PATTERN + ')/(?P<collection_version>' + OclConstants.NAMESPACE_PATTERN + ')/$',    # pylint: disable=C0301
        CollectionDetailView.as_view(), name='collection-version-home')

)
