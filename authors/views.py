from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from .models import Author
from django.contrib.auth.decorators import login_required
from authors.forms import UserForm, AuthorProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.mail import send_mail

#main source: http://www.tangowithdjango.com/book/chapters/login.html

@login_required()
def index(request):
	#TODO: Populate this template with some more information...
	return render(request, 'profile.html')

@login_required()
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
			user.is_active = False
			user.set_password(user.password)

			user.save()

			profile = profile_form.save(commit=False) # False because need to set user attributes ourselves.
			profile.user = user

			if 'profile_pic' in request.FILES:
				profile.profile_pic = request.FILES['profile_pic']

			profile.set_url()

			profile.save()
			registered = True

			# Send email to admin to notify new inactive user registered
			email_subject = 'Account confirmation'
			email_body = 'A new user has been registered with the following information and their account requires activation:\n\nUsername: ' + user.username + ' \nEmail: ' + str(user.email) + ' \n\nClick here to activate the user: https://mighty-cliffs-82717.herokuapp.com/confirm_account/' + user.username

			# send email to admin (will come up with admin email address)
			send_mail(email_subject, email_body, 'cmput404team7@outlook.com',
                ['cmput404team7@outlook.com'], fail_silently=False)

		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = AuthorProfileForm()

	return render_to_response(
		'authors/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
		context)

def confirm_account(request, username):
	try:
		user = User.objects.get(username=username)
		user.is_active = True
		user.save()

		# send email to user to let them know that their account is now activated.
		email_subject = 'MightyCliffs Account Activation'
		email_body = 'Hi %s,\nYour account has now been activated!\nYou can now access your account by logging in here: https://mighty-cliffs-82717.herokuapp.com/ \n\nHave fun!\n\nMightyCliffs'  % (user.username)
		send_mail(email_subject, email_body, 'cmput404team7@outlook.com', 
			[user.email], fail_silently=False)

		return HttpResponse("The following user is now active: " + user.username)
	except User.DoesNotExist:
		return HttpResponse("Cannot find user from this username: " + username)

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
				return HttpResponse("Your Social Dist account is not active yet.")
		else:
			print "Invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied. Cannot log in user!")
	else:
		return render_to_response('authors/login.html', {}, context)

@login_required()
def logout(request):
	# http://stackoverflow.com/questions/31779234/runtime-error-when-trying-to-logout-django 2016-03-04
	django_logout(request)
	return HttpResponseRedirect('/')