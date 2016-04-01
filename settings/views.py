from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.decorators import login_required
from authors.forms import UserForm, AuthorProfileForm
from django.template import RequestContext
from django.shortcuts import render_to_response
from authors.models import Author
from django.contrib.auth.models import User

# Create your views here.

@login_required()
def index(request):

	author = Author.objects.get(user=request.user)
	user =  User.objects.get (id=request.user.id)

	if request.method == 'POST':
		#get all of the form elements
		print "I cannot believe that this could work"
		new_name =  request.POST['username']
		new_git =  request.POST['git_hub']
		new_passwd = request.POST['password']
		#check if the username is not nothing
		if len(new_name) > 0:
			user.username = new_name
		#check if they have a password empy
		if len(new_passwd) > 0:
			user.set_password(new_passwd)

		#condolidate changes
		author.github = new_git
		author.save()
		user.save()

		#generate response
		return HttpResponseRedirect('author/'+author.author_id)
	else:
		return render(request, 'settings/index.html', {'author':author, 'current_author':author})
