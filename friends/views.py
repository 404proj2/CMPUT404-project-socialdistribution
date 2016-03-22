from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from authors.models import Author, GlobalAuthor, LocalRelation, GlobalRelation
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from nodes.models import Node
import requests
from django.conf import settings
import json
import urllib2


@login_required
def index(request):
	# this method also allows user to view local and global friends.
	author = Author.objects.get(user=request.user)

	context = dict()
	context['current_author'] = author
	context['local_friends'] = author.getLocalFriends()
	context['global_friends'] = author.getGlobalFriends()
	context['requests_sent'] = author.getAllPendingFriendRequestsSent()
	context['requests_recieved'] = author.getAllPendingFriendRequestsRecieved()

	if request.POST.get('delete_local'):
		print 'GOT DELETE LOCAL FRIEND REQUEST'
	return render(request, 'friends/index.html', context)

# delete local friend
@login_required
def deleteLocalFriend(request, author_id):
	if request.POST.get('delete_local'):
		author = Author.objects.get(user=request.user)
		delete = Author.objects.get(author_id=author_id)

		# 2 possible ways for 2 local authors to be friends
		try:
			query1 = LocalRelation.objects.get(author1=author, author2=delete, relation_status=True)
			query1.delete()
		except:
			query2 = LocalRelation.objects.get(author1=delete, author2=author, relation_status=True)
			query2.delete()

	context = dict()
	context['current_author'] = author
	context['local_friends'] = author.getLocalFriends()
	context['global_friends'] = author.getGlobalFriends()
	context['requests_sent'] = author.getAllPendingFriendRequestsSent()
	context['requests_recieved'] = author.getAllPendingFriendRequestsRecieved()

	return HttpResponseRedirect('/friends/', context)

# delete global friend
@login_required
def deleteGlobalFriend(request, global_author_id):
	if request.POST.get('delete_global'):
		author = Author.objects.get(user=request.user)
		global_author = GlobalAuthor.objects.get(global_author_id=global_author_id)
		query = GlobalRelation.objects.get(local_author=author, global_author_id=global_author, relation_status=2)
		query.delete()

	context = dict()
	context['current_author'] = author
	context['local_friends'] = author.getLocalFriends()
	context['global_friends'] = author.getGlobalFriends()
	context['requests_sent'] = author.getAllPendingFriendRequestsSent()
	context['requests_recieved'] = author.getAllPendingFriendRequestsRecieved()

	return HttpResponseRedirect('/friends/', context)

# add local user
@login_required
def addLocalFriend(request, author_id):
	if request.POST.get('add_local'):
		query = Author.objects.get(author_id=author_id)
		print 'ADDING WORKS'
		author = Author.objects.get(user=request.user)
		LocalRelation.objects.create(author1=author, author2=query, relation_status=False)
	author = Author.objects.get(user=request.user)

	context = dict()
	context['current_author'] = author
	context['local_friends'] = author.getLocalFriends()
	context['global_friends'] = author.getGlobalFriends()
	context['requests_sent'] = author.getAllPendingFriendRequestsSent()
	context['requests_recieved'] = author.getAllPendingFriendRequestsRecieved()

	return HttpResponseRedirect('/friends/', context)

# add global user
@login_required
def addGlobalFriend(request, global_author_id):
	if request.POST.get('add_global'):
		query = GlobalAuthor.objects.get(global_author_id=global_author_id)
		print 'ADDING GLOBAL WORKS'
		author = Author.objects.get(user=request.user)

		#remote_url = node.node_url + 'authors/'
		#remote_auth = node.basic_auth_token

		#req = urllib2.Request(remote_url)
		#basic_auth_token = 'Basic ' + node.basic_auth_token
		#req.add_header('Authorization', basic_auth_token)

		#sd = urllib2.urlopen(req).read()


		# create a request object in order to send a friend request
		our_url = 'http://ditto-test.herokuapp.com/api/friendrequest'
		print our_url
		print 'TESSSSST'
		requestObj = {
				"query":"friendrequest",
				"author": {
					"id": author.author_id,
					"host": author.host,
					"displayName": author.user.username
				},
				"friend":{
					"id": query.global_author_id,
					"host": query.host,
					"displayName": query.global_author_name,
					"url": query.url
				}
		}
		
		print 'mightcliffs will now try posting a friend request'
		null = 'null'
		r = requests.post(our_url, json=requestObj, auth=('Authorization', 'VGVhbTc6cGFzcw=='))

		print 'request recieved'
		GlobalRelation.objects.create(local_author=author, global_author=query, relation_status=0)

		context = dict()
		context['current_author'] = author
		context['local_friends'] = author.getLocalFriends()
		context['global_friends'] = author.getGlobalFriends()
		context['requests_sent'] = author.getAllPendingFriendRequestsSent()
		context['requests_recieved'] = author.getAllPendingFriendRequestsRecieved()

		return HttpResponseRedirect('/friends/', context)

@login_required
def confirmlocalrequest(request, author_id):
	if request.POST.get('confirm_localrequest'):
		query = Author.objects.get(author_id=author_id)
		print 'CONFIRMING LOCAL WORKS'
		author = Author.objects.get(user=request.user)

		# remove old relationship
		try:
			query1 = LocalRelation.objects.get(author1=author, author2=query, relation_status=False)
			query1.delete()
		except:
			query2 = LocalRelation.objects.get(author1=query, author2=author, relation_status=False)
			query2.delete()

		# Re-add with relation status as mutual friends
		LocalRelation.objects.create(author1=author, author2=query, relation_status=True)

	context = dict()
	context['current_author'] = author
	context['local_friends'] = author.getLocalFriends()
	context['global_friends'] = author.getGlobalFriends()
	context['requests_sent'] = author.getAllPendingFriendRequestsSent()
	context['requests_recieved'] = author.getAllPendingFriendRequestsRecieved()

	return HttpResponseRedirect('/friends/', context)

@login_required
def confirmglobalrequest(request, global_author_id):
	if request.POST.get('confirm_globalrequest'):
		author = Author.objects.get(user=request.user)
		global_author = GlobalAuthor.objects.get(global_author_id=global_author_id)
		query = GlobalRelation.objects.get(local_author=author, global_author_id=global_author, relation_status=1)
		query.delete()

		# Re-add for mutual friends status
		GlobalRelation.objects.create(local_author=author, global_author=global_author, relation_status=2)
		print 'CONFIRMING GLOBAL WORKS'

	context = dict()
	context['current_author'] = author
	context['local_friends'] = author.getLocalFriends()
	context['global_friends'] = author.getGlobalFriends()
	context['requests_sent'] = author.getAllPendingFriendRequestsSent()
	context['requests_recieved'] = author.getAllPendingFriendRequestsRecieved()


	# create a request object in order to send a friend request
	url = 'http://ditto-test.herokuapp.com/api/friendrequest'
	requestObj = {
		"query":"friendrequest",
		"author": {
			"id": author.author_id,
			"host": author.host,
			"displayName": author.user.username
		},
		"friend":{
			"id": global_author.global_author_id,
			"host": global_author.host,
			"displayName": global_author.global_author_name,
			"url": global_author.url
		}
	}
	
	r = requests.post(our_url, json=requestObj, auth=('Authorization', 'VGVhbTc6cGFzcw=='))


	return HttpResponseRedirect('/friends/', context)

@login_required
def search(request):
	# TODO: not finished with this yet.
	if request.method == 'POST':
		search_id = request.POST.get('search_field', None)
		try:
			errors = []
			new_list = []
			# Get all the nodes
			nodes = Node.objects.all()

			# Get all remote users on each node
			for node in nodes:
				try:
					remote_url = node.node_url + 'authors/'
					remote_auth = node.basic_auth_token

					req = urllib2.Request(remote_url)
					basic_auth_token = 'Basic ' + node.basic_auth_token
					req.add_header('Authorization', basic_auth_token)

					sd = urllib2.urlopen(req).read()

					#print 'SD: '
					#print sd

					obj = json.loads(sd)

					#print 'OBJ: '
					#print obj

					for value in obj['authors']:
						print 'Value: '
						print value
						new_list.append(value)
					
					print sd
				except:
					msg = str('Friends could not be loaded from node \'' + node.node_name + '\'. ')
					errors.append(msg)
					print
			# Get all Remote users.


			print new_list

			for item in new_list:
				if GlobalAuthor.objects.filter(global_author_id=item['id']).exists():
					# at least one object satisfying query exists
					print str(item['id']) + ' EXISTS'
				else:
					# no object satisfying query exists
					print "ID NOT FOUND IN GLOBAL AUTHOURS, ADDING...."
					new_global = GlobalAuthor.objects.create(global_author_id=item['id'], global_author_name=item['displayName'], host=item['host'], url=item['url'])
					print item

			all_globals = GlobalAuthor.objects.all()

			global_users = GlobalAuthor.objects.filter(global_author_name__icontains=search_id)
			global_names = []
			for user in global_users:

				global_names.append(user.global_author_name)

			# Get all local authors except the current one.
			local_authors = Author.objects.filter(user__username__icontains=search_id).exclude(user=request.user)

			global_authors = GlobalAuthor.objects.filter(global_author_name__icontains=search_id)
			# Need current user's local and global friends
			author = Author.objects.get(user=request.user)

			# Return all usernames
			context = dict()
			context["query"] = search_id
			context["current_author"] = author
			context["local_authors"] = local_authors
			context["global_authors"] = global_authors
			context["local_friends"] = author.getLocalFriends()
			context['global_friends'] = author.getGlobalFriends()
			return render(request, 'friends/search_results.html', context)

		except User.DoesNotExist:
			return HttpResponse("No such user found.")
	else:
		return render(request, 'friends/index.html')

