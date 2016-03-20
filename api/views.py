from django.http import HttpResponse
from django.shortcuts import render
from authors.models import Author, GlobalAuthor, LocalRelation, GlobalRelation
from posts.models import Post
from comments.models import Comment, GlobalComment
from authors.models import Author, GlobalAuthor
from authors.serializers import AuthorRequestSerializer
from authors.models import LocalRelation, GlobalRelation
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
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

# Default page size
DEFAULT_PAGE_SIZE = 10
# Maximum page size
MAX_PAGE_SIZE = 100
# Default page number
DEFAULT_PAGE_NUM = 0

# TODO: Change this to a static index page, don't return comments here
@api_view(['GET','POST'])
def index(request):
	#return render(request,'api/index.html')
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


''' 
	URL: api/friends/<authorid>
	GET: return boolean if {userid} and authenticated user are friends 
		response:
			responds with: 
			{
				"query":"friends",
				# Array of Author UUIDs
				"authors":[
					"de305d54-75b4-431b-adb2-eb6b9e546013",
					"ae345d54-75b4-431b-adb2-fb6b9e547891"
				],
				# boolean true or false
				"friends": true
			}
	POST: 
'''
@api_view(['GET'])
def queryFriends(request, uuid):
	'''GET returns friends of author_id'''
	try:
		author = Author.objects.get(author_id=uuid)
	except:
		return Response(status=status.HTTP_404_NOT_FOUND)
	friends = author.getLocalFriends()
	#TODO - need to get global friends and concatenate querysets and return

@api_view(['GET'])
def queryFriend2Friend(request, uuid1, uuid2):
	'''ask if 2 authors are friends'''
	if request.method == 'GET':
		#true if uuid1 and uuid2 are both in an entry in LocalRelation or GlobalRelation and relation_status = true
		areFriends = False
		localRelations = LocalRelation.objects.filter((Q(author1__author_id=uuid1) & Q(author2__author_id=uuid2) & Q(relation_status=True)) | (Q(author1__author_id=uuid2) & Q(author2__author_id=uuid1) & Q(relation_status=True)))
		if not localRelations:
			globalRelations = GlobalRelation.objects.filter((Q(local_author__author_id=uuid1) & Q(global_author__global_author_id=uuid2) & Q(relation_status=True)) | (Q(local_author__author_id=uuid2) & Q(global_author__global_author_id=uuid1) & Q(relation_status=True)))
			if globalRelations:
				areFriends = True
		else:
			areFriends = True
		return Response({"query": "friends", "authors":[uuid1, uuid2], "friends": areFriends})

@api_view(['GET'])
def getPosts(request):
	'''Get posts that are visible to current authenticated user'''
	return HttpResponse("getPosts")

@api_view(['GET'])
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
def authorPost(request, uuid):
	'''get all posts made by author_id visible to the current authenticated user'''
	if request.method == 'GET':
		queryID = request.GET.get('id', False)
		print("stupid: %s"%request.GET.get('id', False))
		#need to get all posts uuid can see - PUBLIC, PRIVATE if made by them, posts of FOAF, posts of FRIENDS, posts for SERVERONLY
		posts = Post.objects.filter((Q(visibility="PUBLIC") & Q(author__author_id=uuid)))
		#if queryID == uuid then they can see their private posts
		if queryID == uuid:
			private_posts = Post.objects.filter(Q(visibility="PRIVATE") & Q(author__author_id=uuid))
		#not done
		foaf_posts = Post.objects.filter(Q(visibility="FOAF"))
		serializer = PostSerializer(posts, many=True)
		return Response({"query": "posts", "count": len(posts), "size": 50, "next": "", "previous": "", "posts": serializer.data})

#get and put for update are done
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
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
	elif request.method == 'POST':
		form = PostForm(data=request.POST)
		print(form.errors)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = Author.objects.get(user=request.user.id)
			post.published = timezone.now()
			post.save()
			print(post)
			serializer = PostSerializer(post)
			return Response({"post": serializer.data})

	elif request.method == 'PUT':
		try:
			post = Post.objects.get(post_id=uuid)
		except:
			#TODO - this doesn't work
			#make new post
			serializer = PostSerializer(data=request.data)
			if serializer.is_valid():
				print("I want to make a new post")
				serializer.save(author=request.user)
				return Response(serializer.data)
			print("errors: %s"%serializer.errors)
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		serializer = PostSerializer(post, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		return HttpResponse("hello")
	

#http://www.django-rest-framework.org/tutorial/1-serialization/
#http://www.django-rest-framework.org/tutorial/2-requests-and-responses/
#TODO: size needs to be set, also paging
#TODO: POST should insert post?
#get is done
@api_view(['GET', 'POST'])
def publicPosts(request):
	'''List all public posts on the server'''
	if request.method == 'GET':
		posts = Post.objects.filter(visibility='PUBLIC')
		serializer = PostSerializer(posts, many=True)
		return Response({"query": "posts", "count": len(posts), "size": 50, "next": "", "previous": "", "posts": serializer.data})

	elif request.method == 'POST':
		#TODO - this is not working - should this even insert a post??
		serializer = PostSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

		query = 'comments'
		count = len(all_comments)
		size = page_size

		url = settings.LOCAL_HOST + 'api/posts/' + uuid + '/comments'

		if page.has_next():
			next = url + '?page=' + str(page_num + 1) + '&size=' + str(page_size)
		else:
			next = ''
		if page.has_previous():
			previous = url + '?page=' + str(page_num - 1) + '&size=' + str(page_size)
		else:
			previous = ''

		serializer = CommentSerializer(data, many=True)
		return Response({"query": 'comments', "count": count, "size": size, "next": next, "previous": previous, "comments": serializer.data}, status=status.HTTP_200_OK)
		
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
				url = request.data['author']['url']
				host = request.data['author']['host']
				author = GlobalAuthor(global_author_name = global_author_name, url = url, host = host)
				author.save();

			post = Post.objects.get(post_id=uuid)
			comment = GlobalComment(author=author, post=post)
			
			comment.comment_text = request.data['comment']
			comment.contentType = request.data['contentType']
			comment.save()

			return Response("Comment Successfully Added.", status=status.HTTP_201_CREATED)
		except:
			return Response("Comment not added, bad JSON format.", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def friendRequest(request):
	'''Make a friend request'''
	if request.method == 'POST':
		print 'LOCAL AUTHORS READ 1'
		
		author_id = request.data['author']['id']
		print author_id

		friend_id = request.data['friend']['id']
		print friend_id

		authorObj = None
		friendObj = None
		try:
			authorObj = Author.objects.get(author_id=author_id)
			print 'AUTHOR: '
			print authorObj.user
		except:
			authorObj = GlobalAuthor.objects.get(global_author_id=author_id)
			print 'GLOBAL AUTHOR: '
			print authorObj.global_author_name

		try:
			friendObj = Author.objects.get(author_id=friend_id)
			print 'FRIEND: '
			print friendObj.user
		except:
			friendObj = GlobalAuthor.objects.get(global_author_id=friend_id)
			print 'GLOBAL FRIEND: '
			print friendObj.global_author_name

		if (authorObj.getClassName() == 'Author') and (friendObj.getClassName() == 'Author'):
			print 'both are local, check for existing relationship'
			print authorObj
			print friendObj
			localRelations = LocalRelation.objects.filter((Q(author1=authorObj) & Q(author2=friendObj)) | (Q(author1=friendObj) & Q(author2=authorObj)))

			if localRelations:
				print localRelations
			else:
				localRelations = []

			if len(localRelations) > 0:
				print(len(localRelations))
				# We're assuming author is adding friend so check if author1 != authorObj in order to become friends, otherwise stay following.
				update_local = localRelations[0]

				if update_local.author1 == friendObj and relation_status == False:
					print 'fffffff'
					update_local.relation_status = True
					update_local.save()
					print 'FOLLOW RELATIONSHIP UPDATED!'
				else:
					print 'FRIENDSHIP ALREADY EXISTS!'
			else:
				# Create a local relationship
				LocalRelation.objects.create(author1=authorObj, author2=friendObj, relation_status=False)
				print 'NEW FOLLOW RELATIONSHIP CREATED!'
		else:
			print 'WTF'


		return Response(request.data)

	return HttpResponse("hello")