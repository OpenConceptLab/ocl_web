# -*- coding: utf-8 -*-
""" admin """
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class UserAdmin(admin.ModelAdmin):
    """ UserAdmin class """
    create_form_class = UserCreationForm
    update_form_class = UserChangeForm


admin.site.register(User, UserAdmin)
