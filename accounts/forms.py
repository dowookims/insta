from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        # from django.contrib.auth.models import User
        # setting.Auth_user_model
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']