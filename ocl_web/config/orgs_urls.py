# -*- coding: utf-8 -*-
"""
URL Configuration for "/orgs/..." and all its children.

Regex expression not split across lines -- pylint warnings for long lines supressed
with "# pylint: disable=C0301"

TODO:
- Org and source extras
- Source version for about, details, etc. -- only implemented now for concepts/mappings tabs
- Concepts/mappings & their sub-resources need to be setup to work with source versions
  It may make sense to split this up into separate files to make it simpler to manage --
  then both the org and user URL configs can include the same sub-resource URL config files
- Collections
- What to do with old JSON Angular stuff?
- Clean up views and then remove references here
"""

from __future__ import unicode_literals
from django.conf.urls import (patterns, url)

from apps.orgs.views import (
    OrganizationDetailsView, OrganizationAboutView, OrganizationSourcesView,
    OrganizationNewView, OrganizationEditView, OrganizationRetireView,
    OrganizationMemberAddView, OrganizationMemberRemoveView)

from apps.sources.views import (
    SourceDetailsView, SourceAboutView, SourceConceptsView, SourceMappingsView,
    SourceNewView, SourceEditView, SourceVersionsView,
    SourceVersionsNewView, SourceVersionsEditView, SourceVersionsRetireView)
from apps.concepts.views import (
    ConceptDetailsView, ConceptMappingsView, ConceptHistoryView, ConceptEditView,
    ConceptRetireView, ConceptNewView, ConceptDescView, ConceptNameView)
from apps.mappings.views import (
    MappingDetailsView, MappingNewView, MappingEditView, MappingRetireView)
from apps.core.views import ExtraJsonView


urlpatterns = patterns(
    '',


    ## ORGANIZATION

    # /orgs/new/ - create new org
    url(r'^new/$', OrganizationNewView.as_view(), name='org-new'),

    # /orgs/:org/ - points to /orgs/:org/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/$',
        OrganizationDetailsView.as_view(), name='org-home'),

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

    # /orgs/:org/retire/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/retire/$',
        OrganizationRetireView.as_view(), name='org-retire'),



    ## ORGANIZATION MEMBERS

    # /orgs/:org/members/add/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/add/$',
        OrganizationMemberAddView.as_view(), name='org-member-add'),

    # /orgs/:org/members/remove/:username/ - DOES NOT WORK!
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/remove/(?P<username>[a-zA-Z0-9\-\.]+)/$',
        OrganizationMemberRemoveView.as_view(), name='org-member-remove'),



    ## SOURCES CORE

    # /orgs/:org/sources/new/ - create new source
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/new/$',
        SourceNewView.as_view(), name='source-new'),

    # /orgs/:org/sources/:source/ - points to "source-details"
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/$',
        SourceDetailsView.as_view(), name='source-home'),

    # /orgs/:org/sources/:source/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/details/$',
        SourceDetailsView.as_view(), name='source-details'),

    # /orgs/:org/sources/:source/edit/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$',
        SourceEditView.as_view(), name='source-edit'),

    # /orgs/:org/sources/:source/about/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/about/$',
        SourceAboutView.as_view(), name='source-about'),

    # /orgs/:org/sources/:source/concepts/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/$',
        SourceConceptsView.as_view(), name='source-concepts'),

    # /orgs/:org/sources/:source/:version/concepts/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<source_version>[a-zA-Z0-9\-\.]+)/concepts/$',    # pylint: disable=C0301
        SourceConceptsView.as_view(), name='source-version-concepts'),

    # /orgs/:org/sources/:source/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/$',
        SourceMappingsView.as_view(), name='source-mappings'),

    # /orgs/:org/sources/:source/:version/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/(?P<source_version>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        SourceMappingsView.as_view(), name='source-version-mappings'),

    # /orgs/:org/sources/:source/versions/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/$',
        SourceVersionsView.as_view(), name='source-versions'),

    # /orgs/:org/sources/:source/versions/new/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/new/$',
        SourceVersionsNewView.as_view(), name='source-version-new'),

    # /orgs/:org/sources/:source/:version/edit/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/(?P<source_version>[a-zA-Z0-9\-\.]+)/edit/$',    # pylint: disable=C0301
        SourceVersionsEditView.as_view(), name='source-version-edit'),

    # /orgs/:org/sources/:source/:version/retire/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/(?P<source_version>[a-zA-Z0-9\-\.]+)/retire/$',    # pylint: disable=C0301
        SourceVersionsRetireView.as_view(), name='source-version-retire'),



    # /orgs/:org/sources/:source/extras/ - JSON ONLY - Angular
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/$',
    #    ExtraJsonView.as_view(), name='source-extra'),

    # /orgs/:org/sources/:source/extras/:extra/ - JSON ONLY - Angular
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
    #    ExtraJsonView.as_view(), name='source-extra-add'),



    ## CONCEPTS

    # /orgs/:org/sources/:source/concepts/new/ - create new concept
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/new/$',
        ConceptNewView.as_view(), name='concept-new'),

    # /orgs/:org/sources/:source/concepts/:concept/ - points to "concept-details"
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-home'),

    # /orgs/:org/sources/:source/concepts/:concept/edit/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/edit/$',    # pylint: disable=C0301
        ConceptEditView.as_view(), name='concept-edit'),

    # /orgs/:org/sources/:source/concepts/:concept/retire/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/retire/$',    # pylint: disable=C0301
        ConceptRetireView.as_view(), name='concept-retire'),

    # /orgs/:org/sources/:source/concepts/:concept/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/details/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-details'),

    # /orgs/:org/sources/:source/concepts/:concept/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingsView.as_view(), name='concept-mappings'),

    # /orgs/:org/sources/:source/concepts/:concept/history/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/history/$',    # pylint: disable=C0301
        ConceptHistoryView.as_view(), name='concept-history'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/ - points to "concept-version-details"
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-home'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/details/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-details'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/mappings/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
        ConceptMappingsView.as_view(), name='concept-version-mappings'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/history/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/history/$',    # pylint: disable=C0301
        ConceptHistoryView.as_view(), name='concept-version-history'),



    ## CONCEPT NAMES - old JSON Angular URLs

    # /orgs/:org/sources/:source/concepts/:concept/names/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/names/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/names/:concept-name/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-ud'),

    ## CONCEPT DESCRIPTIONS - old json angular URLs

    # /orgs/:org/sources/:source/concepts/:concept/descriptions/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/descriptions/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/descriptions/:description/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-ud'),

    ## CONCEPT EXTRAS - old json angular URLs

    # /orgs/:org/sources/:source/concepts/:concept/extras/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/extras/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /orgs/:org/sources/:source/concepts/:concept/extras/:extra/ - JSON ANGULAR
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra-add'),


    # PERMALINKS FOR CONCEPT SUB-RESOURCES

    # /orgs/:org/sources/:source/concepts/:concept/names/:name/ - PERMALINK
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-name'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/names/:name/ - PERMALINK
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-name'),

    # /orgs/:org/sources/:source/concepts/:concept/descriptions/:description/ - PERMALINK
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-description'),

    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/descriptions/:description/ - PERMALINK
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<concept_version>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailsView.as_view(), name='concept-version-description'),



    ## MAPPINGS

    # /orgs/:org/sources/:source/mappings/new/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/new/$',    # pylint: disable=C0301
        MappingNewView.as_view(), name='mapping-new'),

    # /orgs/:org/sources/:source/mappings/:mapping/ - points to "mapping-details"
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-home'),

    # /orgs/:org/sources/:source/mappings/:mapping/details/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/details/$',    # pylint: disable=C0301
        MappingDetailsView.as_view(), name='mapping-details'),

    # /orgs/:org/sources/:source/mappings/:mapping/edit/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/edit/$',    # pylint: disable=C0301
        MappingEditView.as_view(), name='mapping-edit'),

    # /orgs/:org/sources/:source/mappings/:mapping/retire/
    url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/retire/$',    # pylint: disable=C0301
        MappingRetireView.as_view(), name='mapping-retire'),



    # TODO(paynejd@gmail.com): Below Mapping URLs are for JSON Angular and are now invalid
    # /orgs/:org/sources/:source/concepts/:concept/mappings/ - JSON ANGULAR
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
    #    ConceptMappingView.as_view(), name='concept-mapping-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/:concept-version/mappings/ - JSON ANGULAR
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/mappings/$',    # pylint: disable=C0301
    #    ConceptMappingView.as_view(), name='concept-mapping-cl'),
    # /orgs/:org/sources/:source/concepts/:concept/mappings/:mapping/ - JSON ANGULAR
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
    #    ConceptMappingView.as_view(), name='concept-mapping-ud'),
    # /orgs/:org/sources/:source/mappings/:mapping/ - JSON ANGULAR
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/mappings/(?P<mapping>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
    #    ConceptMappingView.as_view(), name='mapping-ud'),



    # IMPORTANT: we have to move this to the end because the version value - RETIRE
    # can be misinterpreted as /names/ /descriptions/ etc et. Not great URL design
    #url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/(?P<version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
    #    ConceptDetailView.as_view(), name='concept-details'),
)
