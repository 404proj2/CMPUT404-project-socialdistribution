from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from comments.forms import CommentForm, GlobalCommentForm
from posts.forms import PostForm
from .models import Author
from .models import Post, Comment
from nodes.models import Node
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import timezone
from comments.serializers import CommentSerializer
from datetime import datetime
import uuid
import CommonMark
import urllib2
import json

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

                if comment.contentType == 'text/x-markdown':
                    comment.comment_text =  CommonMark.commonmark(comment.comment_text)

                comment.save()
                return redirect('../../')
        except:
            form = CommentForm(data=request.POST)
            if form.is_valid():

                # TODO: FIX THIS, CHECK FOR OR CREATE GLOBAL AUTHOR
                # MUST ALSO PASS IN THE HOST SO WE CAN RETRIEVE THE CORRECT NODE
                # Get the author of the comment
                #try:
                author = Author.objects.get(user=request.user.id)
                #except:
                #    author, status = GlobalAuthor.objects.get_or_create(user=request.user.id)

                # Create the author dictionary object
                author_dict = {
                    "id": author.author_id,
                    "host": author.host,
                    "displayName": author.user.username, # todo: get the real user name
                    "url": author.url,
                    "github": author.github
                }
                
                # Create the comment dictionary object
                if request.POST.get("contentType") == 'text/x-markdown':
                    comment = CommonMark.commonmark(request.POST.get("comment_text"))
                else:
                    comment = request.POST.get("comment_text")



                comment = {
                    "author": author_dict,
                    "comment": comment,
                    "contentType": request.POST.get("contentType"),
                    "id": uuid.uuid4().hex,
                    "published": str(datetime.now())
                } 

                # Get the node url
                node_name = request.POST.get("node_name")
                node = Node.objects.get(node_name = node_name)
                node_url = node.node_url

                # Get the node's authentication token
                auth_token = "Basic " + str(node.basic_auth_token)

                # Get the post id
                post_id = request.POST.get("post_id")

                # Build the URL to post to
                url = node_url + "posts/" + post_id + "/comments"

                # Create the request object
                req = urllib2.Request(url)
                req.add_header('Content-Type', 'application/json')
                req.add_header('Authorization', auth_token)

                # Jsonify the request
                json_request = json.dumps(comment)
                #print json_request

                # Post to the node
                urllib2.urlopen(req, json_request)
                return redirect('../../')

    else:
        form = CommentForm()



    return render(request, 'authors/index.html', {'form': form})

