from django.db import models
from django.conf import settings
from authors.models import Author, GlobalAuthor
from posts.models import Post
from django.utils import timezone
import uuid

class Comment(models.Model):
	COMMENT_TYPE_CHOICES = (
		('text/x-markdown', 'Markdown'),
		('text/plain', 'Plain text'),
	)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	post =models.ForeignKey(Post, on_delete=models.CASCADE)
	comment_id = models.CharField(max_length=38, unique=True, default=uuid.uuid4)
	pub_date = models.DateTimeField('date published',default=timezone.now)
	comment_text = models.TextField()
	contentType = models.CharField(max_length=20, choices=COMMENT_TYPE_CHOICES,default='text/plain')
	
	def __str__(self):
		return self.comment_text


''' This class is the same as a regualar comment, however it is used for comments
	originating on another server. This is done so that we can associate a comment
	with a GlobalAuthor and not a regular author which requires a user.
'''
class GlobalComment(models.Model):
	COMMENT_TYPE_CHOICES = (
		('text/x-markdown', 'Markdown'),
		('text/plain', 'Plain text'),
	)
	author = models.ForeignKey(GlobalAuthor, on_delete=models.CASCADE)
	post =models.ForeignKey(Post, on_delete=models.CASCADE)
	comment_id = models.CharField(max_length=38, unique=True, default=uuid.uuid4)
	pub_date = models.DateTimeField('date published',default=timezone.now)
	comment_text = models.TextField()
	contentType = models.CharField(max_length=20, choices=COMMENT_TYPE_CHOICES,default='text/plain')

	def __str__(self):
		return self.comment_text