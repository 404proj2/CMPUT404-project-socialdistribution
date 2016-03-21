from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from comments.forms import CommentForm
from posts.forms import PostForm
from .models import Author
from .models import Post, Comment
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import timezone


from django.contrib.auth.models import User

def index(request):
	return HttpResponse("Hello you're at Comment index")


def comment_new(request):
    if request.method == "POST":
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            #comment.post=post
            comment.author = Author.objects.get(user=request.user.id)
            postid = request.POST.get("post_id", "")
            #print("post_id: %s"%postid)
            post = Post.objects.get(post_id=postid)
            #print("post: %s"%post)
            comment.post = post
            comment.pub_date = timezone.now()
            comment.save()
            return redirect('../../')
    else:
        form = CommentForm()
    return render(request, 'authors/index.html', {'form': form})

