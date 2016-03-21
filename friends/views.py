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

		# create a request object in order to send a friend request
		# For now the default is the local host.
		our_url = settings.LOCAL_HOST + 'api/friendrequest'
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
		
		print 'try posting the friend request'
		r = requests.post(our_url, json=requestObj)
		print 'HI'
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

	return HttpResponseRedirect('/friends/', context)

@login_required
def search(request):
	# TODO: not finished with this yet.
	if request.method == 'POST':
		search_id = request.POST.get('search_field', None)
		try:

			# Get all Remote users.
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

