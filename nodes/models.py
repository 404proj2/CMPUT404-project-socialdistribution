from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

class Node(models.Model):
	node_id = models.CharField(max_length=38, unique=True, default=uuid.uuid4)

	# This is the user we create for their node. 
	node_user = models.OneToOneField(User, null=True)

	add_date = models.DateTimeField('date added',default=timezone.now)
	node_name = models.TextField()
	node_url = models.TextField()

	# This is the username/password WE use to access THEIR node
	basic_auth_username = models.TextField(default="")
	basic_auth_password = models.TextField(default="")

	# This will be deprecated and removed soon...
	basic_auth_token = models.TextField(default="")

	# Not implemented yet, will disallow access if we want
	# Right now its done by just changing their user's password
	allow_access = models.BooleanField(default=False)
	
	def __str__(self):
		return self.node_name
