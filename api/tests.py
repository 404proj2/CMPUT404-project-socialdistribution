from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from authors.models import Author, LocalRelation, GlobalRelation, GlobalAuthor
from rest_framework import status
from rest_framework.test import APITestCase
from posts.models import Post
from posts.serializers import PostSerializer
from comments.models import Comment
import urllib
import json,uuid
# Create your tests here.
# http://www.django-rest-framework.org/api-guide/testing/ 2016-03-28
# http://stackoverflow.com/questions/7632315/django-test-client-gets-404-for-all-urls 2016-03-28
class RESTTestCase(TestCase):

	def setUp(self):

		# Local users
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

		user6 = User.objects.create_user(username='user6', password='password')
		author4 = Author.objects.create(user=user6)

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
		post4=Post.objects.create(author=author4,
			                      contentType="content4",
			                      title="title4",
			                      visibility='PUBLIC')

		Comment.objects.create(
                author=author1,
                post=post1,
                comment_text="comment1")
        
		# Global users
		global1, __ = GlobalAuthor.objects.get_or_create(global_author_name='globalusr1', host='http://127.0.0.1:8000/')
		global2, __ = GlobalAuthor.objects.get_or_create(global_author_name='globalusr2', host='http://127.0.0.1:8000/')

		# Create Global Friendship
		GlobalRelation.objects.create(local_author=author1, global_author=global1, relation_status=2)


	# ask a service GET http://service/friends/<authorid>
	def testFriends(self):
		author1 = Author.objects.get(user__username='user1')
		author2 = Author.objects.get(user__username='user2')
		author3 = Author.objects.get(user__username='user3')
		global1 = GlobalAuthor.objects.get(global_author_name='globalusr1')
		
		# Test author1 has friends
		url = '/api/friends/' + author1.author_id
		# print url
		self.client.login(username='user1', password='password')
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertNotEqual(response.data, {})
		self.assertEqual(response.data, { "query":"friends", "authors": [author2.author_id, global1.global_author_id] })

		url = '/api/friends/' + author3.author_id
		# print url
		response = self.client.get(url)

		# Test author3 has no friends
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["authors"], [])


	# Ask if 2 authors are friends
	# GET http://service/friends/<authorid1>/<authorid2>
	def test2Friends(self):
		author1 = Author.objects.get(user__username='user1')
		author2 = Author.objects.get(user__username='user2')
		global1 = GlobalAuthor.objects.get(global_author_name='globalusr1')

		# Test local Friendship
		url = '/api/friends/' + author1.author_id + '/' + author2.author_id
		# print url
		self.client.login(username='user1', password='password')
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, { "query":"friends", "authors": [author1.author_id, author2.author_id], "friends":True })

		# Test global Friendship
		url = '/api/friends/' + author1.author_id + '/' + global1.global_author_id
		# print url
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, { "query":"friends", "authors": [author1.author_id, global1.global_author_id], "friends":True })

		# Test friendship doesn't exist
		url = '/api/friends/' + author2.author_id + '/' + global1.global_author_id
		# print url
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data, { "query":"friends", "authors": [author2.author_id, global1.global_author_id], "friends":False })

	# ask a service if anyone in the list is a friend
	# POST to http://service/friends/<authorid>
	def testCheckListForFriends(self):
		author1 = Author.objects.get(user__username='user1')
		author2 = Author.objects.get(user__username='user2')
		author3 = Author.objects.get(user__username='user3')
		author4 = Author.objects.get(user__username='user4')
		author5 = Author.objects.get(user__username='user5')
		global1 = GlobalAuthor.objects.get(global_author_name='globalusr1')
		global2 = GlobalAuthor.objects.get(global_author_name='globalusr2')

		requestData = { 'query':'friends', 'author': author1.author_id, 'authors': [author2.author_id, global1.global_author_id]}
		print requestData
		url = '/api/friends/' + author1.author_id
		print url
		self.client.login(username='user1', password='password')
		response = self.client.post(url, requestData, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print 'RESPONSE DATA:'
		print response.data
		self.assertEqual(response.data['authors'], [author2.author_id, global1.global_author_id])

		# Test no friends
		requestData = { 'query':'friends', 'author': author3.author_id, 'authors': [author2.author_id, global1.global_author_id]}
		url = '/api/friends/' + author3.author_id
		self.client.login(username='user1', password='password')
		response = self.client.post(url, requestData, format='json')
		self.assertNotEqual(response.data['authors'], [author2.author_id, global1.global_author_id])
		self.assertEqual(response.data['authors'], [])

	def testGetVisiblePosts(self):
		author1=Author.objects.get(user__username='user1')
		post1=Post.objects.filter(author=author1)

	   	url="/api/author/posts/?id="+author1.author_id
	   	self.client.login(username='user1', password='password')
	   	response=self.client.get(url)
	   	self.assertEqual(response.status_code,status.HTTP_200_OK)
	   	self.assertTrue('posts' in response.data,"No 'posts' in response")
	   	self.assertEquals(len(response.data['posts']),4,"should return 4 posts")

	def testpublicPosts(self):
		author1=Author.objects.get(user__username='user1')
		post1=Post.objects.filter(author=author1)
		url="/api/posts/?id="+author1.author_id
		self.client.login(username='user1', password='password')
		response=self.client.get(url)
		print "Public posts"
		print response.data
		self.assertEqual(response.status_code,status.HTTP_200_OK)
		self.assertTrue('posts' in response.data,"No 'posts' in response")
	   	self.assertEquals(len(response.data['posts']),3,"should return 3 posts")

	def testgetProfile(self):
		author1=Author.objects.get(user__username='user1')
		url="/api/author/"+author1.author_id
		self.client.login(username='user1', password='password')
		response=self.client.get(url)
		print 'Profile Response'
		print response.data
		self.assertEqual(response.status_code,status.HTTP_200_OK)


	def testAuthorPosts(self):
		author1=Author.objects.get(user__username='user1')
		url="/api/author/"+author1.author_id+"/posts/?id="+author1.author_id
		self.client.login(username='user1', password='password')
		response=self.client.get(url)
		print 'Author 1 Posts'
		print response.data
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		author2=Author.objects.get(user__username='user2')
		url="/api/author/"+author2.author_id+"/posts/?id="+author2.author_id
		self.client.login(username='user1', password='password')
		response=self.client.get(url)
		print 'Author 2 Posts'
		print response.data
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	def testAllAuthors(self):
		author1=Author.objects.get(user__username='user1')
		url="/api/authors/"
		self.client.login(username='user1', password='password')
		response=self.client.get(url)
		print "All Authors"
		print response.data
		self.assertEqual(response.status_code,status.HTTP_200_OK)

	def testComments(self):
		author1=Author.objects.get(user__username='user1')
		postSet=Post.objects.filter(author=author1)
		commentSet=Comment.objects.filter(post=postSet)
		url="/api/author/"+author1.author_id+"/comments/?id="+author1.author_id
		self.client.login(username='user1', password='password')
		response=self.client.get(url)
		print 'Comments dispalyed'
		print response.data
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(Comment.objects.count(), 1)

	def testGetSinglePost(self):
		author1=Author.objects.get(user__username='user1')
		postSet=Post.objects.filter(author=author1)
		post1 = postSet.first()
		url="/api/posts/"+post1.post_id
		self.client.login(username='user1', password='password')
		response = self.client.get(url)
		print "Get Single post"
		print response.data
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def testDeletePost(self):
		author1=Author.objects.get(user__username='user1')
		postSet=Post.objects.filter(author=author1)
		post1=postSet.first()
		url="/api/posts/"+post1.post_id
		self.client.login(username='user1', password='password')
		response = self.client.delete(url)
		print "deleting??"
		print response.data
		self.assertEqual(response.status_code, status.HTTP_200_OK)


	
       
        

		