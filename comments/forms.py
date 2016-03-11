from django import forms
from .models import Post, Comment

#Adapted from http://tutorial.djangogirls.org/en/django_forms/index.html, March 6, 2016

class CommentForm(forms.ModelForm):
         class Meta:
              model = Comment
              fields = ('comment_text', 'contentType',)
