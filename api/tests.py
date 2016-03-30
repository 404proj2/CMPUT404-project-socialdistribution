from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from authors.models import Author, LocalRelation, GlobalRelation, GlobalAuthor
from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Post
from posts.serializers import PostSerializer
from comments.models import Comment
# Create your tests here.
# http://www.django-rest-framework.org/api-guide/testing/ 2016-03-28
# http://stackoverflow.com/questions/7632315/django-test-client-gets-404-for-all-urls 2016-03-28
class RESTTestCase(TestCase):

	def setUp(self):
		user1 = User.objects.create_user(username='user1', password='password')
		Author.objects.create(user=user1)
		author1 = Author.objects.get(user=user1)

		user2 = User.objects.create_user(username='user2', password='password')
		Author.objects.create(user=user2)
		author2 = Author.objects.get(user=user2)

		user3 = User.objects.create_user(username='user3', password='password')
		author3 = Author.objects.create(user=user3)

		user4 = User.objects.create_user(username='user4', password='password')
		author3 = Author.objects.create(user=user4)

		user5 = User.objects.create_user(username='user5', password='password')
		author3 = Author.objects.create(user=user5)

		# Create Local Friendship
		LocalRelation.objects.get_or_create(author1=author1, author2=author2, relation_status=True)

		post1=Post.objects.create(author=author1,
			                      contentType="content1",
			                      title="title1",
			                      visibility='PUBLIC')
		post2=Post.objects.create(author=author2,
			                      contentType="content2",
			                      title="title2",
			                      visibility='PUBLIC')
		post3=Post.objects.create(author=author1,
			                      contentType="content3",
			                      title="title3",
			                      visibility='PRIVATE')

		Comment.objects.create(
                author=author1,
                post=post1,
                comment_text="comment1")
        
	def testFriends(self):
		author1 = Author.objects.get(user__username='user1')
		author2 = Author.objects.get(user__username='user2')

		url = '/api/friends/' + author1.author_id
		print url
		response = self.client.get(url)
		# views.py: queryFriends(request, uuid)
		self.assertEqual(response.status_code, status.HTTP_200_OK) # should be giving 200...

	def testGetVisiblePosts(self):
		author1=Author.objects.get(user__username='user1')
		post1=Post.objects.filter(author=author1)

	   	url="/api/author/posts/?id="+author1.author_id 
	   	response=self.client.get(url)
	   	self.assertEqual(response.status_code,status.HTTP_200_OK)
	   	self.assertTrue('posts' in response.data,"No 'posts' in response")
	   	self.assertEquals(len(response.data['posts']),3,"should return 3 posts")

	def testpublicPosts(self):
		author1=Author.objects.get(user__username='user1')
		post1=Post.objects.filter(author=author1)
		url="/api/posts/"
		response=self.client.get(url)
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertTrue('posts' in response.data,"No 'posts' in response")
	   	self.assertEquals(len(response.data['posts']),2,"should return 2 posts")

	def testgetProfile(self):
		author1=Author.objects.get(user__username='user1')
		url="/api/author/"+author1.author_id
		response=self.client.get(url)
		self.assertEqual(response.status_code,status.HTTP_200_OK)


	def testAuthorPosts(self):
			author1=Author.objects.get(user__username='user1')
			url="/api/author/"+author1.author_id+"/posts/?id="+author1.author_id
			response=self.client.get(url)
			self.assertEqual(response.status_code, status.HTTP_200_OK)


	
	def test_comments(self):
		author1=Author.objects.get(user__username='user1')
		post1=Post.objects.filter(author=author1)
		url="/api/posts/"+author1.author_id+"/comments/"
		response=self.client.get(url)
		self.assertEqual(response.status_code,status.HTTP_200_OK)

		
