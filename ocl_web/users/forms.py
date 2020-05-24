# -*- coding: utf-8 -*-
"""
    Forms for users.
"""
from allauth.account.adapter import get_adapter
from allauth.account.forms import SignupForm as AllAuthSignupForm
from django.utils.translation import ugettext as _
from django import forms

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


class SignupForm(AllAuthSignupForm):
    def save(self, request):
        """
        Carried from `allauth.account.forms.SignupForm` as of django-allauth==0.15.0.
        We override the view and use this form to stop the form saving EmailAddresses.
        """
        adapter = get_adapter()
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        # formerly
        # super(SignupForm, self).save(user)
        # setup_user_email(request, user, [])
        return user
