from django.test import TestCase
from .models import Author, LocalRelation, GlobalRelation, GlobalAuthor
from django.contrib.auth.models import User

# Source: https://docs.djangoproject.com/en/1.9/topics/testing/overview/ 2016-03-09
class AuthorTestCase(TestCase):

	def setUp(self):
		user1 = User.objects.create(username='user1', password='top_secret')
		author1 = Author.objects.create(user=user1)

		user2 = User.objects.create(username='user2', password='top_secret')
		author2 = Author.objects.create(user=user2)

		user3 = User.objects.create(username='user3', password='top_secret')
		author3 = Author.objects.create(user=user3)

		user4 = User.objects.create(username='user4', password='top_secret')
		author3 = Author.objects.create(user=user4)

		user5 = User.objects.create(username='user5', password='top_secret')
		author3 = Author.objects.create(user=user5)

	def testLocalRelationships(self):

		localusr1 = User.objects.create(username='localusr1', password='top_secret')
		author1 = Author.objects.create(user=localusr1)

		localusr2 = User.objects.create(username='localusr2', password='top_secret')
		author2 = Author.objects.create(user=localusr2)

		localusr3 = User.objects.create(username='localusr3', password='top_secret')
		author3 = Author.objects.create(user=localusr3)

		self.assertEqual(author1.getLocalFriends(), [])
		self.assertEqual(author2.getLocalFriends(), [])

		# Create local friendship
		LocalRelation.objects.create(author1=author1, author2=author2, relation_status=True)
		
		self.assertEqual(author1.getLocalFriends(), [ author2 ])
		self.assertEqual(author2.getLocalFriends(), [ author1 ])

		# author2 added author3 (therefore author2 is following author3)
		LocalRelation.objects.create(author1=author2, author2=author3, relation_status=False)
		self.assertEqual(author2.getLocalFriends(), [ author1 ])

		# Test author1 deleting local friend author2
		query1 = LocalRelation.objects.get(author1=author1, author2=author2, relation_status=True)
		query1.delete()
		self.assertEqual(author1.getLocalFriends(), [])

	def testGlobalRelationships(self):

		localusr1 = User.objects.create(username='localusr1', password='top_secret')
		author1 = Author.objects.create(user=localusr1)

		globalauthor1 = GlobalAuthor.objects.create(global_author_name='globalusr1', host='somehost')

		author1_friends = author1.getGlobalFriends()
		self.assertEqual(author1_friends, [])

		# author1 FOLLOWS globalauthor1 (author1 added globalauthor1 as a friend)
		GlobalRelation.objects.create(local_author=author1, global_author=globalauthor1, relation_status=0)

		self.assertEqual(author1.getGlobalFriends(), [])
		#self.assertEqual(author1.getAllPendingFriendRequestsSent(), [ globalauthor1 ])

		globalauthor2 = GlobalAuthor.objects.create(global_author_name='globalusr2', host='somehost')

		# author1 added globalauthor2 (therefor author1 is following globalauthor2)
		GlobalRelation.objects.create(local_author=author1, global_author=globalauthor2, relation_status=2)
		self.assertEqual(author1.getGlobalFriends(), [ globalauthor2 ])

		# Test author1 deleting global friend globalauthor2
		query1 = GlobalRelation.objects.get(local_author=author1, global_author_id=globalauthor2, relation_status=2)
		query1.delete()
		self.assertEqual(author1.getLocalFriends(), [])

	def testFriendRequestsSent(self):
		localusr1 = User.objects.create(username='localusr1', password='top_secret')
		author1 = Author.objects.create(user=localusr1)

		localusr2 = User.objects.create(username='localusr2', password='top_secret')
		author2 = Author.objects.create(user=localusr2)

		localusr3 = User.objects.create(username='localusr3', password='top_secret')
		author3 = Author.objects.create(user=localusr3)

		sent_requests = author1.getAllPendingFriendRequestsSent()
		self.assertEqual(sent_requests, [])

		# author 1 send a friend request to/follows author2
		LocalRelation.objects.create(author1=author1, author2=author2, relation_status=False)
		self.assertEqual(author1.getAllPendingFriendRequestsSent(), [ author2 ])

		# author 1 sends a friend request to/follows author3
		LocalRelation.objects.create(author1=author1, author2=author3, relation_status=False)
		self.assertEqual(author1.getAllPendingFriendRequestsSent(), [ author2, author3 ])

		globalauthor1 = GlobalAuthor.objects.create(global_author_name='globalusr1', host='somehost')

		# author1 added globalauthor2 (therefor author1 is following globalauthor2)
		GlobalRelation.objects.create(local_author=author1, global_author=globalauthor1, relation_status=0)
		self.assertEqual(author1.getAllPendingFriendRequestsSent(), [ author2, author3, globalauthor1 ])

	def testFriendRequestsRecieved(self):
		localusr1 = User.objects.create(username='localusr1', password='top_secret')
		author1 = Author.objects.create(user=localusr1)

		localusr2 = User.objects.create(username='localusr2', password='top_secret')
		author2 = Author.objects.create(user=localusr2)

		localusr3 = User.objects.create(username='localusr3', password='top_secret')
		author3 = Author.objects.create(user=localusr3)

		recieved_requests = author1.getAllPendingFriendRequestsRecieved()
		self.assertEqual(recieved_requests, [])

		# author 2 send a friend request to/follows author1
		LocalRelation.objects.create(author1=author2, author2=author1, relation_status=False)
		self.assertEqual(author1.getAllPendingFriendRequestsRecieved(), [ author2 ])

		# author 2 send a friend request to/follows author1
		LocalRelation.objects.create(author1=author3, author2=author1, relation_status=False)
		self.assertEqual(author1.getAllPendingFriendRequestsRecieved(), [ author2, author3 ])

		globalauthor1 = GlobalAuthor.objects.create(global_author_name='globalusr1', host='somehost')

		# globalauthor2 added author1(therefor globalauthor2 is following author1)
		GlobalRelation.objects.create(local_author=author1, global_author=globalauthor1, relation_status=1)
		self.assertEqual(author1.getAllPendingFriendRequestsRecieved(), [ author2, author3, globalauthor1 ])


	def testFOAF(self):
		localusr1 = User.objects.create(username='localusr1', password='top_secret')
		author1 = Author.objects.create(user=localusr1)

		localusr2 = User.objects.create(username='localusr2', password='top_secret')
		author2 = Author.objects.create(user=localusr2)

		localusr3 = User.objects.create(username='localusr3', password='top_secret')
		author3 = Author.objects.create(user=localusr3)

		# author1 is friends with author2
		LocalRelation.objects.create(author1=author1, author2=author2, relation_status=True)

		# author2 is friends with author3
		LocalRelation.objects.create(author1=author2, author2=author3, relation_status=True)

		self.assertEqual(author1.isFOAF(author3, False), True)

		# globalauthor1 = GlobalAuthor.objects.create(global_author_name='globalusr1', host='somehost')

		# # author1 is friends with author3
		# GlobalRelation.objects.create(local_author=author1, global_author=author3, relation_status=2)

		# # globalauthor1 is friends with author3
		# GlobalRelation.objects.create(local_author=author3, global_author=globalauthor1, relation_status=2)

		# self.assertEqual(author1.isFOAF(globalauthor1, True), True)
