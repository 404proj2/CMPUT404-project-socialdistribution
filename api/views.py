
# For rest authentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import authentication, permissions

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render
from authors.models import Author, GlobalAuthor, LocalRelation, GlobalRelation
from posts.models import Post
from nodes.models import Node
from comments.models import Comment, GlobalComment
from authors.models import Author, GlobalAuthor
from authors.serializers import AuthorRequestSerializer, FriendSerializer
from authors.models import LocalRelation, GlobalRelation
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
from rest_framework.response import Response
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from django.core.paginator import Paginator
import sys
from itertools import chain
from operator import attrgetter
from django.db.models import Q
from django.conf import settings
import itertools
import CommonMark

# Default page size
DEFAULT_PAGE_SIZE = 10
# Maximum page size
MAX_PAGE_SIZE = 100
# Default page number
DEFAULT_PAGE_NUM = 0


#authentication_classes = (SessionAuthentication, BasicAuthentication)
#permission_classes = (IsAuthenticated,)

# TODO: Change this to a static index page, don't return comments here
@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def index(request):

	content = {
		'user': unicode(request.user),
		'auth': unicode(request.auth),
	}

	print 'User: ', content['user']
	print 'Auth: ', content['auth']

	#node = Node.objects.get(node_user = content['user'])
	#print 'Node: ', node

	''' List all comments '''
	''' TODO: Why is this returning comments? '''



	if request.method == 'GET':
		comments = Comment.objects.all()
		serializer = CommentSerializer(comments, many=True)
		return Response({"comments": serializer.data})
	elif request.method == 'POST':
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def queryFriends(request, uuid):
	'''GET returns friends of author_id'''
	# a reponse if friends or not
	# ask a service GET http://service/friends/<authorid>
	if request.method == 'GET':
		try:
			author = Author.objects.get(author_id=uuid)
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# get local and global friends based on specified uuid
		local_friends = author.getLocalFriends()
		global_friends = author.getGlobalFriends()

		# append all local and global author ids to a list
		friends = []
		for friend in local_friends:
				friends.append(friend.author_id)
		for friend in global_friends:
				friends.append(friend.global_author_id)

		# create expected response object
		response = {
			"query":"friends",
			"authors": friends
		}

		# return response
		return Response(response, status=status.HTTP_200_OK)

	# ask a service if anyone in the list is a friend
	# POST to http://service/friends/<authorid>
	elif request.method == 'POST':
		print 'IN POST FRIEND SEARCH'
		author = None
		try:
			author = Author.objects.get(author_id=uuid)
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# http://stackoverflow.com/questions/13349573/how-to-change-a-django-querydict-to-python-dict 2016-03-29
		recData = dict(request.data.iterlists())
		author_list = recData.get('authors')
		print 'AUTHOR LIST'
		print author_list

		# get local and global friends based on specified uuid
		local_friends = author.getLocalFriends()
		global_friends = author.getGlobalFriends()

		friends = []
		print 'ENTERING FRIEND CHECK'
		for auth in author_list:

			# check in local friends list to compare and add matching IDs to friends list
			for friend in local_friends:
				if friend.author_id == auth:
					print 'LOCAL FRIEND FOUND'
					print auth
					friends.append(auth)

			# check in global friends list to compare and add matching IDs to friends list
			for friend in global_friends:
				if friend.global_author_id == auth:
					print 'GLOBAL FRIEND FOUND'
					print auth
					friends.append(auth)

		# create expected response object
		response = {
			"query":"friends",
			"author":uuid,
			"authors": friends
		}

		# return response
		return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def queryFriend2Friend(request, uuid1, uuid2):
	'''ask if 2 authors are friends'''
	if request.method == 'GET':
		#true if uuid1 and uuid2 are both in an entry in LocalRelation or GlobalRelation and relation_status = true
		areFriends = False
		localRelations = LocalRelation.objects.filter((Q(author1__author_id=uuid1) & Q(author2__author_id=uuid2) & Q(relation_status=True)) | (Q(author1__author_id=uuid2) & Q(author2__author_id=uuid1) & Q(relation_status=True)))
		if not localRelations:
			globalRelations = GlobalRelation.objects.filter((Q(local_author__author_id=uuid1) & Q(global_author__global_author_id=uuid2) & Q(relation_status='2')) | (Q(local_author__author_id=uuid2) & Q(global_author__global_author_id=uuid1) & Q(relation_status='2')))
			if globalRelations:
				areFriends = True
		else:
			areFriends = True
		return Response({"query": "friends", "authors":[uuid1, uuid2], "friends": areFriends})

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def getPosts(request):

	# Page num and size, default if not given
	page_num = request.GET.get('page', DEFAULT_PAGE_NUM)	
	page_size = request.GET.get('size', DEFAULT_PAGE_SIZE)

	# Author id as a query parameter
	queryID = request.GET.get('id', False)
	if queryID:
		try:
		# Get the local author
			author = Author.objects.get(author_id=queryID)
			print author
			# Get all of the authors friends
			local_friends = Author.getLocalFriends(author)
			global_friends = Author.getGlobalFriends(author)

			# Get all of the public posts on the node
			all_posts = Post.objects.filter(visibility="PUBLIC")

			# LOCAL FOAF STUFF
			# Need to go via all local users' local friends first to see if the <author_id> is friends
			all_local_authors = Author.objects.all() # need to exclude self?
			for local_author in all_local_authors:
				print local_author.user

				# get author's global friends and see if the global <author_id> is friends or not.
				localFriends = set(local_author.getLocalFriends())
				
				globalFriendsList = local_author.getGlobalFriends()
				localFriendsList = local_author.getLocalFriends()

				# Already friends
				if author in localFriends:
					all_posts = chain(all_posts, Post.objects.filter(visibility="SERVERONLY", author=local_author))
					all_posts = chain(all_posts, Post.objects.filter(visibility="FRIENDS", author=local_author))
					all_posts = chain(all_posts, Post.objects.filter(visibility="FOAF", author=local_author))
				else:
					# Send POST to /api/friends/<queryID> to check if anyone in the list is a friend
					# check if <author_id> is friends with any one of local_author's friends


					local_author_friends = list(itertools.chain(localFriendsList, globalFriendsList))
					id_list = []

					if len(local_author_friends) > 0:

						for friend in local_author_friends:
							if friend.getClassName() == "Author":
								id_list.append(friend.author_id)
							elif friend.getClassName() == "GlobalAuthor":
								id_list.append(friend.global_author_id)

						requestObj = {
							"query":"friends",
							"author":queryID,
							"authors": id_list
						}

						response = CheckForMutualFriends(requestObj, author)

						FOAF_list = response['authors']
						print "FOAF"
						print FOAF_list

						if len(FOAF_list) > 0:
							# at least 1 mutual friend exists between local <author_id> and local_author
							all_posts = chain(all_posts, Post.objects.filter(visibility="FOAF", author=local_author))
									

			all_posts = list(all_posts)

			# Need this here or else the pagination bitches about it being unicode
			page_num = int(page_num)
			# # Get the right page
			pages = Paginator(all_posts, page_size)
			page = pages.page(page_num+1)
			data = page.object_list
			response_obj = {}
			response_obj['query'] = 'posts'
			response_obj['count'] = len(all_posts)
			response_obj['size'] = page_size

			if page.has_next():
				response_obj['next'] = settings.LOCAL_HOST + 'author/posts/?id=' + queryID + '&page=' + str(page_num + 1) + '&size=' + str(page_size)
			if page.has_previous():
				response_obj['previous'] = settings.LOCAL_HOST + 'author/posts/?id=' + queryID + '&page=' + str(page_num - 1) + '&size=' + str(page_size)

			serializer = PostSerializer(data, many=True)
			response_obj['posts'] = serializer.data

			return Response(response_obj)

			serializer = PostSerializer(all_posts, many=True)
			return Response(serializer.data)
		except:
			print 'why you here'
			print queryID
			author = GlobalAuthor.objects.get(global_author_id = queryID)
			# Get all of the public posts on the node
			all_posts = Post.objects.filter(visibility="PUBLIC")

			# GLOBAL FOAF STUFF
			# Need to go via all local users' global friends first to see if the <author_id> is friends with
			all_local_authors = Author.objects.all() # need to exclude self?
			for local_author in all_local_authors:
				# get author's global friends and see if the global <author_id> is friends or not.
				globalFriends = set(local_author.getGlobalFriends())
				
				globalFriendsList = local_author.getGlobalFriends()
				localFriendsList = local_author.getLocalFriends()

				print "LOCAL AUTHOR IN GLOBAL FOAF STUFF: "
				print local_author.user
				# Already friends
				if author in globalFriends:
					all_posts = chain(all_posts, Post.objects.filter(visibility="FRIENDS", author=local_author))
					all_posts = chain(all_posts, Post.objects.filter(visibility="FOAF", author=local_author))
				else:
					# Send POST to /api/friends/<queryID> to check if anyone in the list is a friend
					# check if <author_id> is friends with any one of local_author's friends

					local_author_friends = list(itertools.chain(localFriendsList, globalFriendsList))

					id_list = []

					if len(local_author_friends) > 0:

						for friend in local_author_friends:
							if friend.getClassName() == "Author":
								id_list.append(friend.author_id)
							elif friend.getClassName() == "GlobalAuthor":
								id_list.append(friend.global_author_id)

						
						requestObj = {
							"query":"friends",
							"author":queryID,
							"authors": id_list
						}

						response = CheckForMutualFriends(requestObj, author)

						FOAF_list = response['authors']
						print "FOAF"
						print FOAF_list

						if len(FOAF_list) > 0:
							# at least 1 mutual friend exists between global <author_id> and local_author
							all_posts = chain(all_posts, Post.objects.filter(visibility="FOAF", author=local_author))
							

			all_posts = list(all_posts)
			# Need this here or else the pagination bitches about it being unicode
			page_num = int(page_num)
			# Get the right page
			pages = Paginator(all_posts, page_size)
			print 'all good here'
			page = pages.page(page_num+1)
			print 'cant see this'
			data = page.object_list
			response_obj = {}
			response_obj['query'] = 'posts'
			response_obj['count'] = len(all_posts)
			response_obj['size'] = page_size

			if page.has_next():
				response_obj['next'] = settings.LOCAL_HOST + 'author/posts/?id=' + queryID + '&page=' + str(page_num + 1) + '&size=' + str(page_size)
			if page.has_previous():
				response_obj['previous'] = settings.LOCAL_HOST + 'author/posts/?id=' + queryID + '&page=' + str(page_num - 1) + '&size=' + str(page_size)

			serializer = PostSerializer(data, many=True)
			response_obj['posts'] = serializer.data

			return Response(response_obj)

			serializer = PostSerializer(all_posts, many=True)
			return Response(serializer.data)
	else:
		#not given a queryID - bad request
		return HttpResponseBadRequest("Need to give id in url: ?id=<author_id>")


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

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def getProfile(request, uuid):
	#View an authors profile
	#try:
	queryAuthor = Author.objects.get(author_id= uuid)
	print(queryAuthor)
	#except:
		#return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		queryAuthor = Author.objects.get(author_id=uuid)
		serializer = AuthorRequestSerializer(queryAuthor)
		print serializer.data
		return Response(serializer.data)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def authorPost(request, uuid):
	'''get all posts made by author_id visible to the current authenticated user'''
	if request.method == 'GET':
		#assuming only local users can create a post on our server, just have to check posts on our server
		#also queryID user must exist on our server, as GlobalAuthor
		queryID = request.GET.get('id', False)
		print'##########################################################################################'
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

				try:
					queryIDuser = Author.objects.get(author_id=queryID)
				except:
					queryIDuser = GlobalAuthor.objects.get(global_author_id=queryID)


				if queryIDuser and local_friend:
					server_posts = Post.objects.filter(Q(visibility="SERVERONLY") & Q(author__author_id=uuid))
					posts = itertools.chain(posts, server_posts)

			# See all accessible, unique posts
			allPosts = list(set(posts))
			#get all FOAF, get all posts that are FOAF
			#if a local user, get all SERVERONLY from friends
			serializer = PostSerializer(allPosts, many=True)
			return Response({"query": "posts", "count": len(allPosts), "size": 50, "next": "", "previous": "", "posts": serializer.data})
		else:
			#not given a queryID - bad request
			return HttpResponseBadRequest("Need to give id in url: ?id=<author_id>")

#get and put for update are done
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def singlePost(request, uuid):
	'''GET returns a single post
	POST inserts a post
	PUT insert/updates a post
	DELETE deletes the post'''
	if request.method == 'GET':
		try:
			post = Post.objects.get(post_id=uuid)
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)
		print(post)
		serializer = PostSerializer(post)
		return Response({"post": serializer.data})

	# elif request.method == 'POST':
	# 	form = PostForm(data=request.POST)
	# 	print(form.errors)
	# 	if form.is_valid():
	# 		post = form.save(commit=False)
	# 		post.author = Author.objects.get(user=request.user.id)
	# 		post.published = timezone.now()
	# 		post.save()
	# 		print(post)
	# 		serializer = PostSerializer(post)
	# 		return Response({"post": serializer.data})

	elif request.method == 'PUT':
		try:
			post = Post.objects.get(post_id=uuid)
		except:
			#TODO - this doesn't work
			#make new post
			# I don't think this should exist anymore
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

			# serializer = PostSerializer(data=request.data)
			# if serializer.is_valid():
			# 	print("I want to make a new post")
			# 	serializer.save(author=request.user)
			# 	return Response(serializer.data)
			# print("errors: %s"%serializer.errors)
			# return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer = PostSerializer(post, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		try:
			post = Post.objects.get(post_id=uuid)
			deleted = Post.objects.get(post_id=uuid).delete()
			return Response("Post deleted", status=status.HTTP_200_OK)
		except:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	

''' 
---------
| POSTS |
---------

GET:	
	** must be sorted newest to oldest
	REQUEST:
		api/posts/
		api/posts/?page=4
		api/posts/?page=4&size=40

	RETURNS:
		{
			"query": "posts",
			"count": 1023,
			"size": 50,
			"next": "http://service/author/posts?page=5",
			"previous": "http://service/author/posts?page=3",
			"posts":[
				{
					"title":"A post title about a post about web dev",
					"source":"http://lastplaceigotthisfrom.com/post/yyyyy",
					"origin":"http://whereitcamefrom.com/post/zzzzz",
					"description":"This post discusses stuff -- brief",
					"contentType":"text/plain",
					"content": "This is the content",
					"author":{
						"id":"de305d54-75b4-431b-adb2-eb6b9e546013",
						"host":"http://127.0.0.1:5454/",
						"displayName":"Lara Croft",
						"url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
						"github": "http://github.com/laracroft"
					},
					"categories":["web","tutorial"],
					"count": 1023,
					"size": 50,
					"next": "http://service/posts/{post_id}/comments",
					"comments":[
						{
							"author":{
								"id":"de305d54-75b4-431b-adb2-eb6b9e546013",
								"host":"http://127.0.0.1:5454/",
								"displayName":"Greg Johnson",
								"url":"http://127.0.0.1:5454/author/9de17f29c12e8f97bcbbd34cc908f1baba40658e",
								"github": "http://github.com/gjohnson"
							},
							"comment":"Sick Olde English",
							"contentType":"text/x-markdown",
							"published":"2015-03-09T13:07:04+00:00",
							"id":"de305d54-75b4-431b-adb2-eb6b9e546013"
						}
					]
					"published":"2015-03-09T13:07:04+00:00",
					"id":"de305d54-75b4-431b-adb2-eb6b9e546013",
					"visibility":"PUBLIC"
				}
			]
		}
'''
# http://www.django-rest-framework.org/tutorial/1-serialization/
# http://www.django-rest-framework.org/tutorial/2-requests-and-responses/
@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def publicPosts(request):

	'''List all public posts on the server'''


	if request.method == 'GET':
		# Default if not given
		page_num = request.GET.get('page', DEFAULT_PAGE_NUM)	
		page_size = request.GET.get('size', DEFAULT_PAGE_SIZE)
		
		# Get all local and global comments, combine and paginate results
		all_posts = Post.objects.filter(visibility='PUBLIC').order_by('-published')

		#for post in all_posts:
		#	print post.comments

		#num_comments = len(all_posts[0]['comments'])

		#print 'Comments: '
		#print num_comments

		# Need this here or else the pagination bitches about it being unicode
		page_num = int(page_num)


		# Get the right page
		pages = Paginator(all_posts, page_size)
		page = pages.page(page_num+1)
		data = page.object_list

		response_obj = {}
		response_obj['query'] = 'posts'
		response_obj['count'] = len(all_posts)
		response_obj['size'] = page_size

		if page.has_next():
			response_obj['next'] = settings.LOCAL_HOST + 'api/posts?page=' + str(page_num + 1) + '&size=' + str(page_size)
		if page.has_previous():
			response_obj['previous'] = settings.LOCAL_HOST + 'api/posts?page=' + str(page_num - 1) + '&size=' + str(page_size)

		serializer = PostSerializer(data, many=True)
		response_obj['posts'] = serializer.data

		return Response(response_obj)


	elif request.method == 'POST':
		'''This method POSTS '''

		
		auth = request.data['author']
		try:
			author = Author.objects.get(author_id = auth)
			print(author)
		except Exception, e:
			print 'No Author!'
			return Response("Not a valid author...", status=status.HTTP_400_BAD_REQUEST)

		try:
			post = Post(author = author)
			

			post.title = request.data['title']
			post.description = request.data['description']
			post.contentType = request.data['contentType']
			post.content  = request.data['content']
			post.visibility = request.data['visibility']
			post.categories = request.data['categories']
			post.set_source()
			post.set_origin()
			post.save()


			#post.set_origin()
			return Response("Post Successfully Added.", status=status.HTTP_201_CREATED)
		except:
			return Response("Post Not Added", status=status.HTTP_400_BAD_REQUEST)



# TODO: Create, save, and return a new GlobalAuthor
def createGlobalAuthor(author):
	return none



''' 
------------
| COMMENTS |
------------

GET:	
	REQUEST:
		api/posts/{post_id}/comments
		api/posts/{post_id}/comments?page=4
		api/posts/{post_id}/comments?page=4&size=40

	RETURNS:
		{
    "count": 11,
    "comments": [
        {
            "author": {
                "id": "9251028c-71d2-45d1-98c6-d71b347148a3",
                "host": "https://mighty-cliffs-82717.herokuapp.com/",
                "displayName": "GlobAuth1",
                "url": "http://www.cool-bears.com"
            },
            "comment": "Sick Olde English",
            "contentType": "text/x-markdown",
            "id": "920431e0-8bea-40df-a315-36ffe6be8c86",
            "published": "2016-03-20T17:38:11.296Z"
        }
    ],
    "next": "https://mighty-cliffs-82717.herokuapp.com/api/posts/f6f32a3b-0d3a-4e35-b229-06389271d7f4/comments?page=3&size=3",
    "query": "comments",
    "size": "1",
    "previous": "https://mighty-cliffs-82717.herokuapp.com/api/posts/f6f32a3b-0d3a-4e35-b229-06389271d7f4/comments?page=1&size=3"
}

POST: 	
	REQUEST:
		api/api/posts/{post_id}/comments
		{
			"author": {
		        "id": "9251028c-71d2-45d1-98c6-d71b347148a3",
		        "host": "http://127.0.0.1:8000/",
		        "displayName": "GlobAuth1",
		        "url": "http://mike.ca",
		        "github": ""
		    },
			"comment":"Sick Olde English",
			"contentType":"text/x-markdown",
			"published":"2015-03-09T13:07:04+00:00",
			"id":"de305d54-75b4-431b-adb2-eb6b9e546013"
		}

	Returns:
		RETURNS:
			HTTP 201 Created
		Failure:
			HTTP 400 Bad Request
'''
@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def comments(request, uuid):
	if request.method == 'GET':

		# Does the post actually exist?
		try:
			p = Post.objects.get(post_id=uuid)
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)

		# Default if not given
		page_num = request.GET.get('page', DEFAULT_PAGE_NUM)	
		page_size = request.GET.get('size', DEFAULT_PAGE_SIZE)
		
		# Get all local and global comments, combine and paginate results
		local_comments = Comment.objects.filter(post=p)
		global_comments = GlobalComment.objects.filter(post=p)

		all_comments = sorted(
	    	chain(local_comments, global_comments),
	    	key=attrgetter('pub_date'))

		# Need this here or else the pagination bitches about it being unicode
		page_num = int(page_num)

		# Get the right page
		pages = Paginator(all_comments, page_size)
		page = pages.page(page_num+1)
		data = page.object_list

		response_obj = {}
		response_obj['query'] = 'comments'
		response_obj['count'] = len(all_comments)
		response_obj['size'] = page_size

		if page.has_next():
			response_obj['next'] = settings.LOCAL_HOST + 'api/posts/' + uuid + '/comments?page=' + str(page_num + 1) + '&size=' + str(page_size)
		if page.has_previous():
			response_obj['previous'] = settings.LOCAL_HOST + 'api/posts/' + uuid + '/comments?page=' + str(page_num - 1) + '&size=' + str(page_size)

		serializer = CommentSerializer(data, many=True)
		response_obj['comments'] = serializer.data

		return Response(response_obj, status=status.HTTP_200_OK)
		
	elif request.method == 'POST':
		try:
			try:
				# Get an existing global author
				author = GlobalAuthor.objects.get(global_author_id=request.data['author']['id'])
				print 'Found existing global author...'
			except:
				# Create a new global author
				global_author_name = request.data['author']['displayName']
				print 'Creating new global author'
				id = request.data['author']['id']
				url = request.data['author']['url']
				host = request.data['author']['host']
				author = GlobalAuthor(global_author_name = global_author_name, url = url, host = host)
				author.save();
				print 'Successfully created author'

			post = Post.objects.get(post_id=uuid)
			print 'Found a post...'
			comment = GlobalComment(author=author, post=post)
			print 'Initialized a comment..'

			if request.data['contentType'] == 'text/x-markdown':
				markedOne= CommonMark.commonmark(request.data['comment'])
				comment.comment_text = markedOne
			else:	
				comment.comment_text = request.data['comment']

			print 'added text..'
			comment.contentType = request.data['contentType']

			print 'Added comment type'
			comment.save()
			print 'Successfully created comment'

			return Response("Comment Successfully Added.", status=status.HTTP_201_CREATED)
		except:
			return Response("Comment not added, bad JSON format.", status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def friendRequest(request):
	'''Make a friend request'''
	if request.method == 'POST':
		print 'LOCAL AUTHORS READ 1'

		print 'AUTHOR'
		print ("id: %s"%request.data['author']['id'])
		print ("host: %s"%request.data['author']['host'])
		print ("displayName: %s"%request.data['author']['displayName'])

		print 'FRIEND'
		print request.data['friend']['id']
		print request.data['friend']['host']
		print request.data['friend']['displayName']
		print request.data['friend']['url']
		
		an_author = request.data['author']
		a_friend = request.data['friend']
		author_id = request.data['author']['id']
		friend_id = request.data['friend']['id']

		print author_id
		print friend_id

		authorObj = None
		friendObj = None

		# Try to get an author/ global author object based on given IDs (author_id, friend_id) for authorObj
		try:
			authorObj = Author.objects.get(author_id=author_id)
			print 'AUTHOR: '
			print authorObj.user
		except:
			print 'GLOBAL AUTHOR: '

			# Check if global author exists, otherwise create it
			try:
				authorObj = GlobalAuthor.objects.get(global_author_id=author_id)
				print 'GLOBAL AUTHOR EXISTS'
			except:
				print "IN EXCEPT"
				GlobalAuthor.objects.create(global_author_id=author_id, global_author_name=an_author['displayName'], host=an_author['host'])
				authorObj = GlobalAuthor.objects.get(global_author_id=author_id)
				print 'GLOBAL AUTHOR CREATED'

			print authorObj.global_author_name

		# Try to get an author/ global author object based on given IDs (author_id, friend_id) for friendObj
		try:
			friendObj = Author.objects.get(author_id=friend_id)
			print 'FRIEND: '
			print friendObj.user
		except:
			print 'GLOBAL FRIEND: '

			# Check if global friend exists, otherwise create it
			if GlobalAuthor.objects.get(global_author_id=friend_id).exists():
				print 'GLOBAL FRIEND EXISTS'
				friendObj = GlobalAuthor.objects.get(global_author_id=friend_id)
			else:
				print 'GLOBAL FRIEND DOESNT EXIST'
				GlobalAuthor.objects.create(global_author_id=friend_id, global_author_name=a_friend['displayName'], host=a_friend['host'], url=a_friend['url'])
				friendObj = GlobalAuthor.objects.get(global_author_id=friend_id)
				print 'GLOBAL FRIEND CREATED'

			print friendObj.global_author_name

		# Deal with friend requests here
		if (authorObj.getClassName() == 'Author') and (friendObj.getClassName() == 'Author'):
			print 'both are local, check for existing relationship'
			localRelations = LocalRelation.objects.filter((Q(author1=authorObj) & Q(author2=friendObj)) | (Q(author1=friendObj) & Q(author2=authorObj)))

			if localRelations:
				print localRelations
			else:
				localRelations = []

			if len(localRelations) > 0:
				print(len(localRelations))
				# We're assuming author is adding friend so check if author1 != authorObj in order to become friends, otherwise stay following.
				update_local = localRelations[0]

				print update_local.author1
				print update_local.author2

				if update_local.author1 == friendObj and update_local.author2 == authorObj and update_local.relation_status == False:
					update_local.relation_status = True
					update_local.save()
					print 'FOLLOW RELATIONSHIP UPDATED - NOW FRIENDS!'
				else:
					print 'FRIENDSHIP ALREADY EXISTS!'
			else:
				# Create a local relationship
				LocalRelation.objects.create(author1=authorObj, author2=friendObj, relation_status=False)
				print 'NEW FOLLOW RELATIONSHIP CREATED!'
		elif (authorObj.getClassName() == 'Author') and (friendObj.getClassName() == 'GlobalAuthor'):
			print 'local wants to add global'

			globalRelations = GlobalRelation.objects.filter(Q(local_author=authorObj) & Q(global_author=friendObj))

			if globalRelations:
				print globalRelations
			else:
				globalRelations = []

			if len(globalRelations) > 0:
				print 'global relation exists.'

				update_global = globalRelations[0]

				print update_global.local_author
				print update_global.global_author
				print update_global.relation_status

				if (update_global.relation_status == '1'): # global author is following local author
					# Therefore global already following local, so now they can be friends.
					update_global.relation_status = 2
				 	update_global.save()
				 	print 'NOW FRIENDS!'

				elif (update_global.relation_status == '2'): # friends
					print 'ALREADY FRIENDS!'

				elif (update_global.relation_status == '0'): # local author is following global author
					print 'LOCAL ALREADY FOLLOWING GLOBAL!'

			else:
				# Create global relationship where local adds global
				GlobalRelation.objects.create(local_author=authorObj, global_author=friendObj, relation_status=0)
				print 'NEW GLOBAL RELATION ADDED'

		elif (authorObj.getClassName() == 'GlobalAuthor') and (friendObj.getClassName() == 'Author'):
			print 'global wants to add local'

			globalRelations = GlobalRelation.objects.filter(Q(local_author=friendObj) & Q(global_author=authorObj))

			if globalRelations:
				print globalRelations
			else:
				globalRelations = []

			if len(globalRelations) > 0:
				print 'global relation exists.'

				update_global = globalRelations[0]

				print update_global.local_author
				print update_global.global_author
				print update_global.relation_status

				if (update_global.relation_status == '0'):
					# Therefore local already following global, so now they can be friends.
					update_global.relation_status = 2
					update_global.save()
					print 'NOW FRIENDS!'

				elif (update_global.relation_status == '2'):
					print 'ALREADY FRIENDS!'

				elif (update_global.relation_status == '1'):
					print 'GLOBAL ALREADY FOLLOWING LOCAL!'

			else:
				# Create global relationship where remote adds local
				GlobalRelation.objects.create(local_author=friendObj, global_author=authorObj, relation_status=1)
				print 'NEW GLOBAL RELATION ADDED'
				return Response(request.data, status=status.HTTP_201_CREATED)

		return Response(request.data)

	return Response("Friend request cannot be processed.", status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
def allAuthors(request):
	'''returns all local users on this node'''
	if request.method == 'GET':
		authors = Author.objects.all()
		serializer = FriendSerializer(authors, many=True)
		return Response({"authors": serializer.data})
