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

@login_required
def index(request):
	author = Author.objects.get(user=request.user)
	return render(request, 'settings/index.html', {'author':author, 'current_author':author})
