from django.db import models
from django.conf import settings
from authors.models import Author
from django.utils import timezone
import uuid

class Post(models.Model):
	POST_TYPE_CHOICES = (
		('text/x-markdown', 'Markdown'),
		('text/plain', 'Plain text'),
	)
	PRIVACY_CHOICES = (
		('PRIVATE', 'Private to me'),
		('AUTHOR', 'Private to another author'),
		('FRIENDS', 'Private to my friends'),
		('FOAF', 'Friend of a friend'),
		('SERVERONLY', 'Private to only friends on my host'),
		('PUBLIC', 'Public'),
	)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	post_id = models.CharField(max_length=38, unique=True, default=uuid.uuid4, primary_key=True)
	published = models.DateTimeField('date published',default=timezone.now)
	content = models.TextField()
	title = models.CharField(max_length=64)
	contentType = models.CharField(max_length=20, choices=POST_TYPE_CHOICES,default='text/plain')
	visibility = models.CharField(max_length=10, choices=PRIVACY_CHOICES,default='PUBLIC')
	source = models.URLField(max_length=140 ,default=settings.LOCAL_HOST)
	origin = models.URLField(max_length=140 ,default=settings.LOCAL_HOST)
	categories = models.CharField(max_length=64, blank = True)
	description = models.CharField(max_length=140, blank=True)
	def __str__(self):
		return self.content
	#def set_source(self):
	#	self.source = str(settings.LOCAL_HOST) + "post/" +str(post_id)
	#def set_origin(self):
	#	self.origin = str(settings.LOCAL_HOST) + "post/" + str(post_id)


