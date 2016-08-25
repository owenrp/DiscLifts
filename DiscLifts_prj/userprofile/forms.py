from django import forms
from .models import UserProfile
from django.contrib.auth.models import User



class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        # exclude the user field from the form
        exclude = ('user',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', ]
