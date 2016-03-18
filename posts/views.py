from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PostForm
from .models import Author
from comments.models import Comment
from .models import Post
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	return HttpResponse("Hello you're at posts index")

#adapted from http://tutorial.djangogirls.org/en/django_forms/index.html
@login_required
def post_new(request):
	if request.method == "POST":
		form = PostForm(data=request.POST)
		print(form)
		print(form.errors)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = Author.objects.get(user=request.user.id)
			post.published = timezone.now()
			post.save()
			#return redirect('show_posts')
			return HttpResponseRedirect(reverse('show_posts'))
			#return render(request, 'authors/index.html', {'form':form})
	else:
		form = PostForm()
	return render(request, 'authors/index.html', {'form':form})

@login_required
def show_posts(request):
	print "gets to this point"
	auth = Author.objects.get(user=request.user)
	posts = Post.objects.filter(author=auth).order_by('-published')

	for p in posts:
		p.comments = Comment.objects.filter(post=p.post_id)

	#comments = Comment.objects.all()
	context = dict()
	context['current_author'] = auth
	context['posts'] = posts
	#context['comments'] = comments
	#print posts
	return render(request,'authors/index.html', context)

@login_required
def delete_post(request):
	if request.method == "POST":
		print("id: %s"%request.POST.get("post_id"))
		post = Post.objects.get(post_id=request.POST.get("post_id"))
		print post
		if post != None:
			post.delete()
			return HttpResponseRedirect(reverse('show_posts'))
		else:
			#TODO: this should return 404
			return HttpResponseRedirect(reverse('show_posts'))

		

