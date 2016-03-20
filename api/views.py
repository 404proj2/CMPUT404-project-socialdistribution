from django.http import HttpResponse
from django.shortcuts import render
from authors.models import Author, GlobalAuthor, LocalRelation, GlobalRelation
from posts.models import Post
from comments.models import Comment
from authors.models import Author
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
import sys
from django.db.models import Q

#http://www.django-rest-framework.org/tutorial/1-serialization/
#don't need this anymore
class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@api_view(['GET','POST'])
def index(request):
	'''List all comments'''
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
	return 'hello'

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
	if request.method ==  'GET':
		posts =  Post.objects.filter()
		serializer = PostSerializer(posts, many=True)
		return Response({"posts": serializer.data})


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

#done
@api_view(['GET'])
def comments(request, uuid):
	'''Returns all the comments for this post id'''
	try:
		queryPost = Post.objects.get(post_id=uuid)
	except:
		return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		comments = Comment.objects.filter(post=queryPost)
		serializer = CommentSerializer(comments, many=True)
		return Response({"query": "comments", "count": len(comments), "size": 50, "next": "", "previous": "", "comments": serializer.data})

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