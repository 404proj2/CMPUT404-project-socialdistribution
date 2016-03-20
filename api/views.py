from django.http import HttpResponse
from django.shortcuts import render
from posts.models import Post
from comments.models import Comment, GlobalComment
from authors.models import GlobalAuthor
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
	return HttpResponse("hello")

@api_view(['GET'])
def getPosts(request):
	'''Get posts that are visible to current authenticated user'''
	return HttpResponse("hello")

@api_view(['GET'])
def getProfile(request, uuid):
	'''View an author's profile'''
	return HttpResponse("hello")

@api_view(['GET'])
def authorPost(request, uuid):
	'''get all posts made by author_id visible to the current authenticated user'''
	return HttpResponse("hello")

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

@api_view(['GET', 'POST'])
def comments(request, uuid):
	if request.method == 'GET':
		'''Returns all the comments for this post id'''
		# TODO: This DOESNT WORK, never returns any comments
		try:
			queryPost = Post.objects.get(post_id=uuid)
		except:
			return Response(status=status.HTTP_404_NOT_FOUND)
		comments = Comment.objects.filter(post=queryPost.post_id)
		serializer = CommentSerializer(comments, many=True)
		return Response({"query": "comments", "count": len(comments), "size": 50, "next": "", "previous": "", "comments": serializer.data})
	elif request.method == 'POST':
		#print "Raw Request Body: "
		#print request.data
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

			if author == None:
				# Global author doesn't exist, have to create one...
				print 'No Author!'
				return Response("Not a valid author...", status=status.HTTP_400_BAD_REQUEST)

			#print 'AUTHOR'
			#print author
			post = Post.objects.get(post_id=uuid)
			#print 'POST'
			#print post
			comment = GlobalComment(author=author, post=post)
			#print comment.author
			#print comment.post
			
			comment.comment_text = request.data['comment']
			comment.contentType = request.data['contentType']
			print comment.author
			print comment.post
			print comment.comment_text
			print comment.contentType

			comment.save()
			#data = serializers.serialize("json", comment, indent=4)
			#comment.pub_date = timezone.now()
	        #author = GlobalAuthor.objects.all()
	        #print author
	        # Associate to the correct author
	        #if author:
	        #	comment.author = author
	        #else:
	        #	createGlobalAuthor(request.data.author)
	        
	        # Associate to the correct post
	        #post = Post.objects.get(post_id=postid)
	        #comment.post = post

	        # Save the comment
	        #print comment.comment_text 
	        #comment.save()
			return Response("Comment Successfully Added.", status=status.HTTP_201_CREATED)
		except:
			return Response("Comment Not Added", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def friendRequest(request):
	'''Make a friend request'''
	return HttpResponse("hello")