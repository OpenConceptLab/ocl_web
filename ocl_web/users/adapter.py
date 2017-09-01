import re

from django.utils.translation import ugettext_lazy as _
from django import forms
from config import settings

from allauth.account.adapter import DefaultAccountAdapter
from urlparse import urlsplit, urlunsplit

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

    def send_mail(self, template_prefix, email, context):
        if 'activate_url' in context:
            context['activate_url'] = settings.BASE_URL + \
                                  '/accounts/confirm-email/' + context['key']
        if 'password_reset_url' in context:
            reset_url = context['password_reset_url']
            split_url = reset_url.split('/')
            del split_url[0:3]
            context['password_reset_url'] = settings.BASE_URL + '/' + '/'.join(split_url)

        msg = self.render_mail(template_prefix, email, context)
        msg.send()
