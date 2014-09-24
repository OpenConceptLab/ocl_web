# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from allauth.account.signals import (user_signed_up, user_logged_in, email_confirmed)
from .signals import (user_created_handler, user_logged_in_handler,
                        email_confirmed_handler)

# Subclass AbstractUser
class User(AbstractUser):
    """
    This is the extended Django user on the web application, so that
    we can add additional data and behavior to the base user model.

    Each front end django user has a corresponding user entry in the
    API backend.
    """

    def __unicode__(self):
        return self.username

    def save_auth_token(self, request, token):
        """ Save API user token into session table for online use.

            :param request: is the django http request
            :param token: is the backend auth token.
        """
        request.session['API_USER_TOKEN'] = token

    def get_auth_token(self, request):
        """ Get previously seaved API user token for accessing OCL API.

            :param request: is the django http request
            :returns: auth token or maybe the anonymous user token?
        """
        return request.session.get('API_USER_TOKEN', '???')



# Hook up signals to django-allauth
user_signed_up.connect(user_created_handler)
email_confirmed.connect(email_confirmed_handler)
user_logged_in.connect(user_logged_in_handler)