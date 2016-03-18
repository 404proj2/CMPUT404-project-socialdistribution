from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

class Node(models.Model):
	node_id = models.CharField(max_length=38, unique=True, default=uuid.uuid4)
	add_date = models.DateTimeField('date added',default=timezone.now)
	node_name = models.TextField()
	node_url = models.TextField()
	
	def __str__(self):
		return self.node_name
