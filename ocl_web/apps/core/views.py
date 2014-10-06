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
