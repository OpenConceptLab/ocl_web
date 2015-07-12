# -*- coding: utf-8 -*-
"""
URL Configuration for "/users/" and all its children.

Regex expression not split across lines -- pyline warnings supressed using "# pylint: disable=C0301"
"""

from django.conf.urls import patterns, url

from users.views import (
    UserListView, UserRedirectView, UserDetailView, UserUpdateView)
from apps.sources.views import (
    SourceDetailView, SourceCreateView, SourceEditView)
from apps.sources.views import (SourceVersionView)
from apps.concepts.views import (
    ConceptDetailView, ConceptCreateView, ConceptEditView, ConceptCreateJsonView)
from apps.concepts.views import (
    ConceptDescView, ConceptNameView, ConceptVersionListView)
from apps.core.views import ExtraJsonView


urlpatterns = patterns(
    '',

    ## USER CORE

    # /users/:user/sources/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/new/$',
        SourceCreateView.as_view(), name='source-create-for-user'),

    # /users/:user/sources/:source/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/$',
        SourceDetailView.as_view(), name='source-detail'),

    # /users/:user/sources/:source/edit/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/edit/$',
        SourceEditView.as_view(), name='source-edit'),

    # /users/:user/sources/:source/versions/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/$',
        SourceVersionView.as_view(), name='source-version-cl'),

    # /users/:user/sources/:source/versions/:source-version/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/versions/(?P<version>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        SourceVersionView.as_view(), name='source-version-ud'),


    ## SOURCE EXTRAS

    # /users/:user/sources/:source/extras/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/$',
        ExtraJsonView.as_view(), name='source-extra'),
    # /users/:user/sources/:source/extras/extra/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='source-extra-add'),


    ## CONCEPTS

    # /users/:user/sources/:source/create/
    # TODO(paynejd@gmail.com): Change this to: /users/:user/sources/:source/new-concept/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/create/$',
        ConceptCreateJsonView.as_view(), name='concept-create-for-user'),
    # /users/:user/sources/:source/concepts/:concept/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDetailView.as_view(), name='concept-detail'),
    # /users/:user/sources/:source/concepts/:concept/edit/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/edit/$',    # pylint: disable=C0301
        ConceptCreateJsonView.as_view(), name='concept-edit'),
    # /users/:user/sources/:source/concepts/:concept/versions/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/versions/$',    # pylint: disable=C0301
        ConceptVersionListView.as_view(), name='concept-version-list'),


    ## CONCEPT NAMES

    # /users/:user/sources/:source/concepts/:concept/names/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-cl'),
    # /users/:user/sources/:source/concepts/:concept/names/:concept-name/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/names/(?P<name>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptNameView.as_view(), name='concept-name-ud'),


    ## CONCEPT DESCRIPTIONS

    # /users/:user/sources/:source/concepts/:concept/descriptions/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-cl'),
    # /users/:user/sources/:source/concepts/:concept/descriptions/:concept-description/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/descriptions/(?P<description>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ConceptDescView.as_view(), name='concept-desc-ud'),


    ## CONCEPT EXTRAS

    # /users/:user/sources/:source/concepts/:concept/extras/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra'),
    # /users/:user/sources/:source/concepts/:concept/extras/:extra/
    url(r'^(?P<user>[a-zA-Z0-9\-\.]+)/sources/(?P<source>[a-zA-Z0-9\-\.]+)/concepts/(?P<concept>[a-zA-Z0-9\-\.]+)/extras/(?P<extra>[a-zA-Z0-9\-\.]+)/$',    # pylint: disable=C0301
        ExtraJsonView.as_view(), name='concept-extra-add'),


    ## ??

    # URL pattern for the UserListView
    url(
        regex=r'^$',
        view=UserListView.as_view(),
        name='list'
    ),
    # URL pattern for the UserRedirectView
    url(
        regex=r'^~redirect/$',
        view=UserRedirectView.as_view(),
        name='redirect'
    ),
    # URL pattern for the UserDetailView
    url(
        regex=r'^(?P<username>[\w@\.\+\-_]+)/$',
        view=UserDetailView.as_view(),
        name='detail'
    ),
    # URL pattern for the UserUpdateView
    url(
        regex=r'^update/(?P<username>[\w@\.\+\-_]+)/$',
        view=UserUpdateView.as_view(),
        name='update'
    ),
)
