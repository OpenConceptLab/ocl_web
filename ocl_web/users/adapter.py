import re

from django.utils.translation import ugettext_lazy as _
from django import forms

from allauth.account.adapter import DefaultAccountAdapter


class OCLAccountAdapter(DefaultAccountAdapter):
    """
    A custom adapter for django-allauth so that we can limit username
    to a smaller set of allowed characters for the API.
    """

    def clean_username(self, username):
        """
        Validates the username. You can hook into this if you want to
        (dynamically) restrict what usernames can be chosen.
        """
        username_regex = r'^[a-zA-Z0-9\-\.]+$'
        if not re.match(username_regex, username):
            raise forms.ValidationError(_("Usernames can only contain "
                                          "letters, digits and . -"))

        return super(OCLAccountAdapter, self).clean_username(username)
