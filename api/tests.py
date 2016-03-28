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

	def testFriends(self):
		author1 = Author.objects.get(user__username='user1')
		author2 = Author.objects.get(user__username='user2')

		url = '/friends/' + author1.author_id
		print url
		response = self.client.get(url)
		# views.py: queryFriends(request, uuid)
		self.assertEqual(response.status_code, status.HTTP_200_OK) # should be giving 200...
