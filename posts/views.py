from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PostForm, ImageForm
from .models import Author
from comments.models import Comment, GlobalComment
from .models import Post, Image
from posts.serializers import PostsDeserializer
from comments.serializers import CommentSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
import CommonMark
from django.conf import settings
from authors.models import GlobalAuthor,LocalRelation, GlobalRelation
from posts.converter import PostConverter
from itertools import chain
from operator import attrgetter
from nodes.models import Node
import urllib2
from itertools import chain
from operator import attrgetter
from django.db.models import Q
from django.conf import settings
import itertools
#import json

from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser

@login_required()
def index(request):
	return HttpResponse("Hello you're at posts index")

#adapted from http://tutorial.djangogirls.org/en/django_forms/index.html
@login_required()
def post_new(request):
	if request.method == "POST":
		form = PostForm(data=request.POST)

		#print("REQUEST.POST:%s"%request.POST)
		imageForm = ImageForm(request.POST, request.FILES)
		#print("FILES: %s"%request.FILES['imageFile'])


		#print(form)
		#print(form.errors)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = Author.objects.get(user=request.user.id)
			post.published = timezone.now()
			if post.contentType == 'text/x-markdown':
				post.content =  CommonMark.commonmark(post.content)
			post.set_source()
			post.set_origin()
			post.save()
			if request.POST['image_url']:
				post.content = post.content + "<br><img src="+"'"+request.POST['image_url']+"'"+"/>"
			post.save()
			#return redirect('show_posts')
			#return render(request, 'authors/index.html', {'form':form})
			if imageForm.is_valid():
				image = Image(imageFile=request.FILES['imageFile'])
				image.post = post
				image.save()
				content = post.content
				print("image url: %s"%image.imageFile.url)
				imgUrl = "https://mighty-cliffs-82717.herokuapp.com/media/" + image.imageFile.url
				#this will work for mighty cliffs but not for local testing
				#imgUrl = post.source + "media/"+image.imageFile.url
				print("imgUrl: %s"%imgUrl)
				post.content = content + "<br><img src="+"'"+imgUrl+"'"+"/>"
				post.save()
				print("post.content: %s"%post.content)
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/')
	else:

		form = PostForm()
	return render(request, 'authors/index.html', {'form':form})

@login_required()
def show_posts(request):
	print "gets to this point"
	auth = Author.objects.get(user=request.user)
	posts = Post.objects.filter(author=auth).order_by('-published')

	for p in posts:
		p.comments = Comment.objects.filter(post=p.post_id)

	#comments = Comment.objects.all()
	context = dict()
	context['current_author'] = auth
	context['posts'] = posts
	#context['comments'] = comments
	#print posts
	return render(request,'authors/index.html', context)

@login_required()
def delete_post(request):
	if request.method == "POST":
		print("id: %s"%request.POST.get("post_id"))
		post = Post.objects.get(post_id=request.POST.get("post_id"))
		print post
		if post != None:
			post.delete()
			return HttpResponseRedirect('/')
		else:
			#TODO: this should return 404
			return HttpResponseRedirect('/')


@login_required()
def show_profile(request,uuid):
	try:
		queryAuth = Author.objects.get(author_id=uuid)

		
		curAuth = Author.objects.get(user=request.user)

		

			
		if queryAuth == curAuth:

			all_posts = []
			posts= Post.objects.filter(author=queryAuth).order_by('-published')
			for p in posts:
				local_comments = Comment.objects.filter(post=p.post_id)
				global_comments = GlobalComment.objects.filter(post=p.post_id)
				p.comments = sorted(
			    chain(local_comments, global_comments),
			    	key=attrgetter('pub_date'))

			for post in posts:
				all_posts.append(post)

			#print all_posts[0].comments
			list.sort(all_posts)

			context = dict()
			context['current_author'] = curAuth
			context['posts'] = all_posts
			return render(request,'authors/index.html', context)
			
		else:
			'''
			context['current_author'] = queryAuth
			context['authorName'] = queryAuth.user.username
			print queryAuth.user.username
			return render(request,'authors/profile.html', context)
			'''
		
			posts, errors, localAuth = getInternalPosts(uuid, request)
			print "Makes it back out"
			context = dict()
			context['current_author'] = localAuth
			context['posts'] = posts
			context['authorName'] = queryAuth.user.username
			return render(request,'authors/profile.html', context)


	except:
		print "okay"

		posts, errors, globalAuth = getExternalPosts(uuid, request)
		print "Makes it back out"
		context = dict()
		context['current_author'] = globalAuth
		context['posts'] = posts
		context['authorName'] = globalAuth.global_author_name
		return render(request,'authors/profile.html', context)



def getExternalPosts(uuid, request):
	curAuth = Author.objects.get(user=request.user)
	queryAuth = GlobalAuthor.objects.get(global_author_id=uuid)
	host = queryAuth.host
	node = str(host)+"api/"
	postConv = PostConverter()
	posts = []
	errors = []
	print "error after this"
	n = Node.objects.get(node_url=node)
	url = node + 'author/' +str(uuid) + '/posts?id='+curAuth.author_id
	req = urllib2.Request(url)
	print url
	basic_auth_token = 'Basic ' + n.basic_auth_token
	req.add_header('Authorization', basic_auth_token)
	#print 'authorizes'
	
	

	sd = urllib2.urlopen(req).read()
	#sd = urllib2.urlopen(url).read()
	#print 'sends request'
	stream = BytesIO(sd)
	data = JSONParser().parse(stream)
	#print "breaks"
	serializer = PostsDeserializer(data=data)
	#print serializer

	serializer.is_valid()
	#print "is it?"
	print "before the return"
	for p in serializer.data['posts']:
		#print p
		p['server'] = n.node_name
		post = postConv.convert(p)
		print post
		posts.append(post)

	#msg = str('Posts could not be loaded from node \'' + n.node_name + '\'. ')
	#errors.append(msg)
	
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

	return posts, errors, queryAuth

def getInternalPosts(uuid, request):
	errors = []
	queryID = Author.objects.get(user=request.user)
	print queryID
	if queryID:
		#need to get all posts uuid can see - PUBLIC, PRIVATE if made by them, posts of FOAF, posts of FRIENDS, posts for SERVERONLY
		posts = Post.objects.filter((Q(visibility="PUBLIC") & Q(author__author_id=uuid)))
		#if queryID == uuid then they can see their private posts
		if queryID == uuid:
			private_posts = Post.objects.filter(Q(visibility="PRIVATE") & Q(author__author_id=uuid))
			posts = itertools.chain(posts, private_posts)
		user = Author.objects.get(author_id=uuid)
		if user:
			#then they are a local user, need to check if user and uuid are friends, then can return FRIENDS and FOAF posts
			global_friend = GlobalRelation.objects.filter(Q(local_author__author_id=uuid) & Q(global_author__global_author_id=queryID) & Q(relation_status='2'))
			local_friend = LocalRelation.objects.filter((Q(author1__author_id=uuid) & Q(author2__author_id=queryID) & Q(relation_status=True)) | (Q(author1__author_id=queryID) & Q(author2__author_id=uuid) & Q(relation_status=True)))
			if global_friend or local_friend:
				#then uuid and queryID are friends, can return all FRIENDS and FOAF posts
				friend_posts = Post.objects.filter((Q(visibility="FRIENDS") | Q(visibility="FOAF")) & Q(author__author_id=uuid))
				posts = itertools.chain(posts, friend_posts)
			#if queryID user is also local, then can see all SERVERONLY if they are friends

			globalFriendsList = []
			globalFriendsList = user.getGlobalFriends()

			localFriendsList = []
			localFriendsList = user.getLocalFriends()

			all_friends = list(itertools.chain(localFriendsList, globalFriendsList))

			id_list = []

			if len(all_friends) > 0:

				for friend in all_friends:
					if friend.getClassName() == "Author":
						id_list.append(friend.author_id)
					elif friend.getClassName() == "GlobalAuthor":
						id_list.append(friend.global_author_id)
				
				requestObj = {
					"query":"friends",
					"author":queryID,
					"authors": id_list
				}

				response = CheckForMutualFriends(requestObj, user)


				FOAF_list = response['authors']
				print "FOAF"
				print FOAF_list

				if len(FOAF_list) > 0:
					# at least 1 mutual friend exists between global <author_id> and user
					posts = chain(posts, Post.objects.filter(visibility="FOAF", author=user))

			print("gets here")
			#queryIDuser = Author.objects.get(author_id=queryID)



			if queryID and local_friend:
				server_posts = Post.objects.filter(Q(visibility="SERVERONLY") & Q(author__author_id=uuid))
				posts = itertools.chain(posts, server_posts)

		# See all accessible, unique posts
		allPosts = list(set(posts))

	return posts, errors, queryID


@login_required()
def add_image(request):
	if request.method == 'POST':
		form = ImageForm(request.POST, request.FILES)
		print("FILES: %s"%request.FILES['imageFile'])
		print("POST: %s"%request.POST)
		if form.is_valid():
			image = Image(imageFile=request.FILES['imageFile'])
			print("HELLO")
			image.save()
			return HttpResponse('image upload success')
		else:
			print("not valid form")
			print("errors: %s"%form.errors)
			curAuth = Author.objects.get(user=request.user)
			context = dict()
			context['current_author'] = curAuth
			return HttpResponse("hello")


def CheckForMutualFriends(requestObj, authorObj):
	print 'IN POST FRIEND SEARCH'
	author = authorObj
	author_list = requestObj['authors']
	print 'AUTHOR LIST'
	print author_list

	# get local and global friends based on specified uuid, works also for global.
	local_friends = author.getLocalFriends()

	global_friends = []
	if author.getClassName() == 'Author':
		global_friends = author.getGlobalFriends()

	friends = []
	print 'ENTERING FRIEND CHECK'
	for auth in author_list:

		# check in local friends list to compare and add matching IDs to friends list
		for friend in local_friends:
			if friend.author_id == auth:
				friends.append(auth)

		# check in global friends list to compare and add matching IDs to friends list
		for friend in global_friends:
			if friend.global_author_id == auth:
				friends.append(auth)

	print 'preparing response'
	# create expected response object

	if author.getClassName() == 'Author':
		response = {
			"query":"friends",
			"author":author.author_id,
			"authors": friends
		}
	else:
		response = {
			"query":"friends",
			"author":author.global_author_id,
			"authors": friends
		}

	# return response
	return response