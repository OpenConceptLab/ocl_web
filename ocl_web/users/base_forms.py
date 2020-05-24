"""
Pull BaseSignupForm here to prevent circular import between us and django-allauth
"""

from django.utils.translation import ugettext as _
from django import forms

from .models import User


class BaseSignupForm(forms.ModelForm):
    """
    Custom form for user to sign up for an account.
    Used by django-allauth as a **base class** for their signup form
    """
    required_css_class = 'required'

    first_name = forms.CharField(max_length=30, label=_('First Name'), required=True)
    last_name = forms.CharField(max_length=30, label=_('Last Name'), required=True)

    class Meta:
        """ Meta class """
        # Set this form to use the User model.
        model = User

        # Constrain the UserForm to just these fields.
        fields = ("first_name", "last_name")

    def signup(self, request, user):
        """ signup """
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

    def save(self, user):
        """ save """
        print 'In SignupForm save:', user.username
        print user.first_name, user.email
        return user
