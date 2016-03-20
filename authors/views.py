from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from .models import Author
from django.contrib.auth.decorators import login_required
from authors.forms import UserForm, AuthorProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response

#main source: http://www.tangowithdjango.com/book/chapters/login.html

@login_required
def index(request):
	return render(request, 'profile.html')

@login_required
def view_user_profile(request):
	# This page should have author's (user's) profile, and
	# display the author's posts only.
	context = dict()
	author = Author.objects.get(user=request.user)
	context['current_author'] = author
	# context['profile_pic'] = author.get_absolute_image_url()
	author.save()
	return render(request, 'authors/profile.html', context)

def register(request):
	context = RequestContext(request)
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = AuthorProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save();

			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False) # False because need to set user attributes ourselves.
			profile.user = user

			if 'profile_pic' in request.FILES:
				profile.profile_pic = request.FILES['profile_pic']

			profile.set_url()

			profile.save()


			registered = True
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = AuthorProfileForm()

	return render_to_response(
		'authors/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
		context)

def user_login(request):
	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				# send user back to home page -- should
				# be changed to user's profile page but
				# this will do for now.
				return HttpResponseRedirect('/')
			else:
				return HttpResponse("Your Social Dist account is disabled.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied. Cannot log in user!")
	else:
		return render_to_response('authors/login.html', {}, context)

@login_required
def logout(request):
	# http://stackoverflow.com/questions/31779234/runtime-error-when-trying-to-logout-django 2016-03-04
	django_logout(request)
	return HttpResponseRedirect('/')