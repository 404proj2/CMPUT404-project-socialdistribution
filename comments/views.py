from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from comments.forms import CommentForm, GlobalCommentForm
from posts.forms import PostForm
from .models import Author
from .models import Post, Comment
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import timezone
from comments.serializers import CommentSerializer


from django.contrib.auth.models import User

def index(request):
	return HttpResponse("Hello you're at Comment index")


def comment_new(request):
    if request.method == "POST":


        try:
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
        except:
            form = CommentForm(data=request.POST)
            if form.is_valid():

                # Get the author
                author = Author.objects.get(user=request.user.id)

                # Get the post
                postid = request.POST.get("post_id", "")
                post = Post(post_id = postid, author=author)

                comment = Comment.objects.create(author = author, post = post)

                #comment.author = Author.objects.get(user=request.user.id)
                #post = Post(post_id=postid, author=comment.author)
                #comment.post = post
                comment.pub_date = timezone.now()
                
                serializer = CommentSerializer(comment)
                #if serializer.is_valid():
                #    serializer.save()
                print serializer.data



                return redirect('../../')



    else:
        form = CommentForm()



    return render(request, 'authors/index.html', {'form': form})

