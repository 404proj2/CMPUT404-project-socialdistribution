from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from posts.forms import PostForm
from authors.models import Author
from nodes.models import Node
from comments.models import Comment
from posts.models import Post
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.core import serializers

import urllib2
import json

#@login_required
#def index(request):
#	return render(request, 'stream/index.html')

def getExternalPosts():

	nodes = Node.objects.all()

	posts = []

	for n in nodes:
		url = n.node_url + 'posts/'
		sd = urllib2.urlopen(url).read()
		#serializers.deserialize("json", serialized_data, ignorenonexistent=True)
		
		serialized_data = '[' + sd + ']'
		print serialized_data



		#for obj in serializers.deserialize("json", serialized_data):
		#    print obj

		# data should be the unserialized list of Post objects
		#data = json.loads(serialized_data)
		#posts.append(data)
		#print data


	return posts

def byDate(self, other):
	return other.published > self.published

@login_required
def index(request):
	author = Author.objects.get(user=request.user)

	# Will hold all of the posts after processing them
	all_posts = []
	
	# Get local posts and attach the comments
	int_posts = Post.objects.filter(published__lte=timezone.now()).order_by('-published')
	for p in int_posts:
		p.server = "Local"
		p.comments = Comment.objects.filter(post=p.post_id)

	for post in int_posts:
		all_posts.append(post)
	getExternalPosts()
	# Get external posts
	ext_posts = Post.objects.filter(published__lte=timezone.now()).order_by('-published')#getExternalPosts()
	for post in ext_posts:
		post.server = "Remote"
		all_posts.append(post)

	list.sort(all_posts)
	
	# Combine the two lists in chronological order
	#while int_posts and ext_posts:

		#if int_posts[0].published < ext_posts[0].published:
		#	all_posts.append(int_posts.pop())
		#else:
		#	all_posts.append(ext_posts.pop())

	#if int_posts:
	#	all_posts.append(int_posts)

	#if ext_posts:
	#	all_posts.append(ext_posts)

	context = dict()
	context['current_author'] = author
	context['posts'] = all_posts

	return render(request,'stream/index.html', context)