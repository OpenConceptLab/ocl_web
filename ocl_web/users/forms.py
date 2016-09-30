# -*- coding: utf-8 -*-
"""
    Forms for users.
"""
from django.utils.translation import ugettext as _
from django import forms
#from django.core.urlresolvers import reverse

from .models import User

class UserForm(forms.Form):
    """ User edit form """
    required_css_class = 'required'

    first_name = forms.CharField(max_length=30, label=_('First Name'), required=True)
    last_name = forms.CharField(max_length=30, label=_('Last Name'), required=True)
    email = forms.EmailField(max_length=30, label=_('Email'), required=True)
    company = forms.CharField(max_length=30, label=_('Company'), required=False)
    location = forms.CharField(max_length=30, label=_('Location'), required=False)
    #preferred_locale = forms.CharField(max_length=30, label=_('Preferred Locale'), required=False)

    def clean_email(self):
        """ email must be unique """
        data = self.cleaned_data['email']
        try:
            u = User.objects.get(email=data)
            if u.username != self.initial['username']:
                raise forms.ValidationError(
                    _('This email is already used by a different account.'))
        except User.DoesNotExist:
            pass
        return data


class SignupForm(forms.ModelForm):
    """
    Custom form for user to sign up for an account, used by django-allauth
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
