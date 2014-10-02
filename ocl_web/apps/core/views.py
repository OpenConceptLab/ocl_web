class UserOrOrgMixin(object):
    """                                                                                                                   
    Figure out if a view is called from a user or an organization "owner".

    """
    def get_args(self):
        """
            Are we called from org or user?
            Set for variables in the view.

        """
        self.from_user = False
        self.from_org = False
        self.user_id = self.org_id = None

        self.org_id = self.kwargs.get('org')
        if self.org_id is None:
            self.user_id = self.kwargs.get('user')
            self.from_user = True
        else:
            self.from_org = True



