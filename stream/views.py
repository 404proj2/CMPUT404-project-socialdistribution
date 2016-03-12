from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from posts.forms import PostForm
from authors.models import Author
from comments.models import Comment
from posts.models import Post
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

#@login_required
#def index(request):
#	return render(request, 'stream/index.html')

@login_required
def index(request):
	print "gets to this point"
	author = Author.objects.get(user=request.user)
	posts = Post.objects.filter(published__lte=timezone.now()).order_by('-published')

	for p in posts:
		p.comments = Comment.objects.filter(post=p.post_id)

	#comments = Comment.objects.all()
	#comments = Comment.objects.filter(post=)
	context = dict()
	context['current_author'] = author
	context['posts'] = posts
	#context['comments'] = comments
	#print posts
	return render(request,'stream/index.html', context)