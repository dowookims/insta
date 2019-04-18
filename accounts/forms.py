from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        # from django.contrib.auth.models import User
        # setting.Auth_user_model
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'nickname','image']