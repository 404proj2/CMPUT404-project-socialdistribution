from authors.models import Author
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class AuthorProfileForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('profile_pic',)