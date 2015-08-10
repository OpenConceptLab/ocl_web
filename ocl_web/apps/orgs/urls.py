"""
Organization urls
TODO: Retire this file!
"""
#from django.conf.urls import patterns, url, include
#from django.views.generic import TemplateView
#from .views import OrganizationDetailsView, OrganizationNewView

# TODO(paynejd@gmail.com): I believe this file is retired...

# urlpatterns = patterns('',

# 	Create new organization - /orgs/new/
#     url(r'^new/$', OrganizationNewView.as_view(), name='org-new'),

#     Create new organization - /orgs/create/ - RETIRE
#     TODO(paynejd@gmail.com): Retire old URL for creating new organizations
#     url(r'^create/$', OrganizationNewView.as_view(), name='org-new'),

#     Detailed Org View - /orgs/CIEL/
#     url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/$', OrganizationDetailsView.as_view(), name='org-details'),

#     RETIRED
# 	url(r'^$', OrganizationListView.as_view(), name='organization-list'),
# 	url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/$', UserListView.as_view(), {'related_object_type': Organization, 'related_object_kwarg': 'org', 'related_object_attribute': 'members'}, name='organization-members'),
# 	url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/members/(?P<user>[a-zA-Z0-9\-]+)/$', OrganizationMemberView.as_view(), name='organization-member-detail'),
# 	url(r'^(?P<org>[a-zA-Z0-9\-\.]+)/collections/', include('apps.conceptcollections.urls')),
# )
