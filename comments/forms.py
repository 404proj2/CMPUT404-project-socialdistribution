from django import forms
from .models import Post, Comment, GlobalComment

#Adapted from http://tutorial.djangogirls.org/en/django_forms/index.html, March 6, 2016

class CommentForm(forms.ModelForm):
         class Meta:
              model = Comment
              fields = ('comment_text', 'contentType',)

class GlobalCommentForm(forms.ModelForm):
	class Meta:
		model = GlobalComment
		fields = ('comment_text', 'contentType',)