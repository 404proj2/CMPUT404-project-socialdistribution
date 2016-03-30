from django.test import TestCase
from django.contrib.auth.models import User
from authors.models import Author, LocalRelation, GlobalRelation, GlobalAuthor
from rest_framework import status
from rest_framework.test import APITestCase
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

		# Create Local Friendship
		LocalRelation.objects.get_or_create(author1=author1, author2=author2, relation_status=True)

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
		response = self.client.post(url, requestData, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		print 'RESPONSE DATA:'
		print response.data
		self.assertEqual(response.data['authors'], [author2.author_id, global1.global_author_id])