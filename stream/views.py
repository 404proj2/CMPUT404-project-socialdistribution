from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from posts.forms import PostForm
from authors.models import Author
from nodes.models import Node
from posts.serializers import PostsDeserializer
from comments.serializers import CommentSerializer
from comments.models import Comment, GlobalComment
from posts.models import Post
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from posts.converter import PostConverter
from itertools import chain
from operator import attrgetter
#from django.core import serializers

import urllib2
#import json

from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

#@login_required
#def index(request):
#	return render(request, 'stream/index.html')

def convert(post_dict):
	post = {}

	post.title = post_dict.title
	return post

def getExternalPosts():

	nodes = Node.objects.all()
	postConv = PostConverter()
	posts = []
	errors = []

	for n in nodes:
		url = n.node_url + 'posts/'
		req = urllib2.Request(url)
		basic_auth_token = 'Basic ' + n.basic_auth_token
		req.add_header('Authorization', basic_auth_token)
		
		try:
			sd = urllib2.urlopen(req).read()
			#sd = urllib2.urlopen(url).read()
			
			stream = BytesIO(sd)
			data = JSONParser().parse(stream)

			serializer = PostsDeserializer(data=data)

			serializer.is_valid()

			for p in serializer.data['posts']:
				p['server'] = n.node_name
				post = postConv.convert(p)
				print post
				posts.append(post)
		except Exception, exc_value:
			msg = str('Posts could not be loaded from node \'' + n.node_name + '\'. ')
			errors.append(msg)
		
		'''
		sd = urllib2.urlopen(req).read()
		#sd = urllib2.urlopen(url).read()
		
		stream = BytesIO(sd)
		data = JSONParser().parse(stream)

		serializer = PostsDeserializer(data=data)

		serializer.is_valid()
		
		for p in serializer.data['posts']:
			p['server'] = n.node_name
			post = postConv.convert(p)
			posts.append(post)
			'''

	return posts, errors

def byDate(self, other):
	return other.published > self.published

@login_required()
def index(request):
	author = Author.objects.get(user=request.user)

	# Will hold all of the posts after processing them
	all_posts = []
	
	# Get local posts and attach the comments
	int_posts = Post.objects.filter(published__lte=timezone.now()).order_by('-published')
	for p in int_posts:
		p.server = "Local"
		local_comments = Comment.objects.filter(post=p.post_id)
		global_comments = GlobalComment.objects.filter(post=p.post_id)
		p.comments = sorted(
	    chain(local_comments, global_comments),
	    	key=attrgetter('pub_date'))

	for post in int_posts:
		all_posts.append(post)
	
	# Get external posts
	ext_posts, errors = getExternalPosts()# Post.objects.filter(published__lte=timezone.now()).order_by('-published')#getExternalPosts()
	#for post in ext_posts:
	#
	#	print post.comments
	#	post.server = "Remote"

	#all_posts = chain(all_posts, ext_posts)

	#print all_posts[0].comments
	#list.sort(all_posts)
	all_posts = chain(all_posts, ext_posts)

	
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
	context['errors'] = errors
	context['posts'] = all_posts
	context['requests_recieved'] = author.getAllPendingFriendRequestsRecieved()

	if len(author.github) > 0:
		context['g_hub'] = author.github
	else:
		context['g_hub'] = '404proj2'

	return render(request,'stream/index.html', context)