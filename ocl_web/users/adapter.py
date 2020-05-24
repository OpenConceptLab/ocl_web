import logging
import re

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django import forms
from config import settings

from allauth.account.adapter import DefaultAccountAdapter

from libs.ocl import OclApi


logger = logging.getLogger('oclweb')


class OCLAccountAdapter(DefaultAccountAdapter):
    """
    A custom adapter for django-allauth so that we can;
     1. limit username to a smaller set of allowed characters for the API.
     2. create users using the API and not in the DB.
    """

    def save_user(self, request, user, form, commit=True):
        user = super(OCLAccountAdapter, self).save_user(request, user, form, commit=False)
        ocl = OclApi(admin=True, debug=True)
        data = {
            'username': user.username,
            'email': user.email,
            'hashed_password': user.password,
            'name': '%s %s' % (user.first_name, user.last_name),  # not great
        }

        result = ocl.create_user(data)
        if result.status_code == 201:
            authenticated_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data["password1"])
            # don't return a new user object because the old one was passed to us
            # and we cannot control whether or not the caller continues to use it
            user.backend = authenticated_user.backend
            user.ocl_api_token_object = authenticated_user and authenticated_user.ocl_api_token_object
            return user
        # elif result.status_code == 400:
        #     # todo: agree on cleaner way of handling account re-activations,
        #        leaving this here for context into what we were doing before.
        #     result = ocl.reactivate_user(user.username)
        #     if result != 204:
        #         return

        result.raise_for_status()

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

    def confirm_email(self, request, email_address):
        """
        Marks the email address as confirmed on the db
        """
        logger.debug("Email Confirmed signal for %s", request.user.username)
