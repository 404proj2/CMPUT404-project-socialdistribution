from django import forms
from .models import Post

#Adapted from http://tutorial.djangogirls.org/en/django_forms/index.html, March 6, 2016
class PostForm(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('content', 'title', 'contentType', 'visibility',)

class ImageForm(forms.Form):
	imageFile = forms.ImageField()