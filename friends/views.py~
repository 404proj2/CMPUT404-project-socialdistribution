from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from authors.models import Author, GlobalAuthor, LocalRelation, GlobalRelation
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect

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
		query = Author.objects.get(author_id=author_id)
		query.delete()
	author = Author.objects.get(user=request.user)

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
		query = GlobalAuthor.objects.get(global_author_id=global_author_id)
		query.delete()

	author = Author.objects.get(user=request.user)
	print author.author_id

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
		GlobalRelation.objects.create(local_author=author, global_author=query, relation_status=0)

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
			context["local_authors"] = local_authors
			context["global_authors"] = global_authors
			context["local_friends"] = author.getLocalFriends()
			context['global_friends'] = author.getGlobalFriends()
			return render(request, 'friends/search_results.html', context)

		except User.DoesNotExist:
			return HttpResponse("No such user found.")
	else:
		return render(request, 'friends/index.html')
