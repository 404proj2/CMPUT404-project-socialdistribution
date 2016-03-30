from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
import uuid

class Node(models.Model):
	node_id = models.CharField(max_length=38, unique=True, default=uuid.uuid4)

	node_user = models.OneToOneField(User, null=True)

	add_date = models.DateTimeField('date added',default=timezone.now)
	node_name = models.TextField()
	node_url = models.TextField()
	basic_auth_token = models.TextField(default="")

	allow_access = models.BooleanField(default=False)
	
	def __str__(self):
		return self.node_name
