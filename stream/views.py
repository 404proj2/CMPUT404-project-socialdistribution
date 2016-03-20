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

	for n in nodes:
		url = n.node_url + 'posts/'
		sd = urllib2.urlopen(url).read()
		
		stream = BytesIO(sd)
		data = JSONParser().parse(stream)

		#print sd

		serializer = PostsDeserializer(data=data)

		serializer.is_valid()
		
		#deserialized = serializer.validated_data
		#print 'Deserialized Data: '
		#print serializer.data['posts'][0]
		#print serializer.data['posts']
		
		for p in serializer.data['posts']:
			p['server'] = 'Remote'
			post = postConv.convert(p)
			posts.append(post)


		#deserialized = serializer.validated_data.items()[1]

		#print deserialized

		#for post in deserialized[1]:
		#	p = convert(post)
		#	posts.append(p)

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
		local_comments = Comment.objects.filter(post=p.post_id)
		global_comments = GlobalComment.objects.filter(post=p.post_id)
		p.comments = sorted(
	    chain(local_comments, global_comments),
	    	key=attrgetter('pub_date'))

	for post in int_posts:
		all_posts.append(post)
	
	# Get external posts
	ext_posts = getExternalPosts()# Post.objects.filter(published__lte=timezone.now()).order_by('-published')#getExternalPosts()
	for post in ext_posts:
		print post.comments
	#	post.server = "Remote"

	#print all_posts[0].comments
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