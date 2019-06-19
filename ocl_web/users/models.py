""" Users models """
# -*- coding: utf-8 -*-

from django.contrib.auth.models import AbstractUser
#from django.utils.translation import ugettext_lazy as _

from allauth.account.signals import (user_signed_up, user_logged_in, email_confirmed, password_reset)
from .signals import (user_created_handler, user_logged_in_handler, email_confirmed_handler, user_password_reset_handler)


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


# Hook up signals to django-allauth
user_signed_up.connect(user_created_handler)
email_confirmed.connect(email_confirmed_handler)
user_logged_in.connect(user_logged_in_handler)
password_reset.connect(user_password_reset_handler)