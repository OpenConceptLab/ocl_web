""" Users models """
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser, update_last_login
from django.contrib.auth.signals import user_logged_in as django_auth_signals_user_logged_in

from allauth.account.signals import user_logged_in, email_confirmed, password_reset
from .signals import (user_logged_in_handler, email_confirmed_handler, user_password_reset_handler)


# Subclass AbstractUser
class User(AbstractUser):
    """
    This is the extended Django user on the web application, so that
    we can add additional data and behavior to the base user model.
    """
    # used to pass this object between the (APIAuthBackend or AccountAdapter) and the post login handler
    ocl_api_token_object = None

    def __unicode__(self):
        return self.username

    @property
    def pk(self):
        """
        The Django auth system uses this as the session id and
        passes it to out backend to fetch the user on every request.

        Fallback to something we know for those situations.
        """
        return super(User, self).pk or self.username

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        raise NotImplementedError("User management is done via the API so you should probably not be calling this.")


# Hook up signals to django-allauth
email_confirmed.connect(email_confirmed_handler)
user_logged_in.connect(user_logged_in_handler)
password_reset.connect(user_password_reset_handler)

# disconnect this receiver because it attempts to update the last_login and save: we're not storing user objects anymore
django_auth_signals_user_logged_in.disconnect(update_last_login)
