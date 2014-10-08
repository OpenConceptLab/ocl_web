import requests
import logging

from django.views.generic.edit import View
from django.utils.translation import ugettext as _
from braces.views import JsonRequestResponseMixin

from libs.ocl import OCLapi


logger = logging.getLogger('oclweb')


class UserOrOrgMixin(object):
    """
    Figure out if a view is called from a user or an organization "owner".

    """
    def get_args(self):
        """
            Are we called from org or user? Useful helper for most views.

            Set the following:
            :param self.from_user: set to true/false depending on source type
            :param self.from_org: set to true/false depending on source type
            :param self.org_id: set to org id if source is from org
            :param self.user_id: set to org id if source is from user

            :param self.own_type: set to "owners" or "organizations", good for calling API
            :param self.own_id: set to user id or org id, good for calling API

            :param self.source_id: set to source ID if view URL has source part.
            :param self.concept_id: set to concept ID if view URL has concept part.

        """
        self.from_user = False
        self.from_org = False
        self.user_id = self.org_id = None
        self.own_type = self.own_id = None

        self.org_id = self.kwargs.get('org')
        if self.org_id is None:
            self.user_id = self.kwargs.get('user')
            self.from_user = True
            self.own_type = 'users'
            self.own_id = self.user_id
        else:
            self.from_org = True
            self.own_type = 'orgs'
            self.own_id = self.org_id

        self.source_id = self.kwargs.get('source')
        self.concept_id = self.kwargs.get('concept')


class ExtraJsonView(JsonRequestResponseMixin, UserOrOrgMixin, View):
    """
        Extra handling for org/user/source is different from concept...

        The extras field name IS the attribute name, the data is stored as a dictionary.
        So in this view, we translate the API style of data to be like descriptions and names.
        e.g.:

        API version:   {'price': 100}
        front end version: {extra_name: 'price', extra_value: 100}
    """

    def get_all_args(self):
        """
        Get all the input entities' identity, figure out whether this is a user owned
        sourced concept or an org owned sourced concept, and set self.own_type, self.own_id
        for easy interface to OCL API.
        """
        self.get_args()
        self.extra_id = self.kwargs.get('extra')

    def build_url(self, *args):
        """
            A tricky bit of code here. The extra maybe for
              * an org
              * a user,
              * a source (owned by org or user),
              * a concept
              ...etc...

            We will use what's given in the kwargs in the URL to figure out the
            corresponding OCL API url.
        """
        url_args = [self.own_type, self.own_id]  # either org or user
        if self.source_id is not None:
            url_args += ['sources', self.source_id]
        if self.concept_id is not None:
            url_args += ['concepts', self.concept_id]
        url_args.append('extras')
        if len(args) > 0:
            url_args += args
        return url_args

    def is_edit(self):
        return self.extra_id is not None

    def get(self, request, *args, **kwargs):
        """
            Return a list of descriptions as json.
        """
        self.get_all_args()
        api = OCLapi(self.request, debug=True)

        result = api.get(*self.build_url())
        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        # convert OCLAPI dictionary style data to a list of dictionary objects
        # so that we can use the same front end JS to work with extras.
        ls = []
        for k, v in result.json().iteritems():
            print k, v
            o = {'extra_name': k, 'extra_value': v}
            ls.append(o)

        return self.render_json_response(ls)

    def post(self, request, *args, **kwargs):

        self.get_all_args()

        # Convert back to OCLAPI format for extras, the dictionnary
        # key is the attribute name.
        data = {}
        fn = fv = None
        try:
            print 'request json:', self.request_json
            fn = self.request_json.get('extra_name')
            fv = self.request_json.get('extra_value')
            data[fn] = fv
        except KeyError:
            resp = {'message': _('Invalid input')}
            return self.render_bad_request_response(resp)

        api = OCLapi(self.request, debug=True)
        if self.is_edit():
            result = api.put(*self.build_url(fn), **data)
            msg = _('Extra updated')
        else:
            result = api.put(*self.build_url(fn), **data)
            msg = _('Extra added')

        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)
        else:
            return self.render_json_response({'message': msg})

    def delete(self, request, *args, **kwargs):
        """
        Delete the specified item.
        """
        self.get_all_args()

        api = OCLapi(self.request, debug=True)
        self.extra_id = None
        if not self.is_edit():  # i.e. has item UUID
            return self.render_bad_request_response({'message': 'key missing'})

        result = api.delete(self.own_type, self.own_id, 'sources', self.source_id,
                            'concepts', self.concept_id,
                            'extras', self.extra_id)
        if not result.ok:
            logger.warning('Extra GET failed %s' % result.content)
            return self.render_bad_request_response(result.content)

        return self.render_json_response({'message': _('extra deleted')})
