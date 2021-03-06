from django.test import TestCase

# Create your tests here.
from django.db import models
from comments.models import Comment
from posts.models import Post
from authors.models import Author, LocalRelation
from django.test import Client
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

import collections

import json
import uuid

class CommentTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create(username='user1', password='top_secret')
	author1 = Author.objects.create(user=user1)
        
        user2 = User.objects.create(username='user2', password='top_secret')
	author2 = Author.objects.create(user=user2)

        user3 = User.objects.create(username='user3', password='top_secret')
        author3 = Author.objects.create(user=user3)

	user4 = User.objects.create(username='user4', password='top_secret')
	author3 = Author.objects.create(user=user4)

	user5 = User.objects.create(username='user5', password='top_secret')
	author3 = Author.objects.create(user=user5)

	LocalRelation.objects.get_or_create(author1=author1,
	                                           author2=author2,
	                                           relation_status=True)
	 
	LocalRelation.objects.get_or_create(author1=author1,
	                                           author2=author3,
	                                           relation_status=False)
	       
	LocalRelation.objects.get_or_create(author1=author2,
	                                           author2=author3,
	                                           relation_status=True)
        # Post Set up
        post1 = Post.objects.create(author=author1, 
                                    contentType="content1",
                                    title="title1",                                    
                                    visibility='PUBLIC')
        post2 = Post.objects.create(author=author2, 
                                    contentType="content2",
                                    title="title2",                                   
                                    visibility='PRIVATE')
        post3 = Post.objects.create(author=author3, 
                                    contentType="content3",
                                    title="title3",                                                         
                                    visibility='PRIVATE')
        Comment.objects.create(
                author=author1,
                post=post1,
                comment_text="comment1")
        
        Comment.objects.create(
                author=author1,
                post=post1,
                comment_text="comment2")
        
        Comment.objects.create(
                author=author1,
                post=post2,
                comment_text="comment3")
    
    def testcreate_comments(self):
        c = Client()
        response = c.post('/author/posts/post_new', {'title': '1', 'description': 'comments','contentType': 'add','comments': 'comments' })
    
    def testGetSingleComment(self):
        'test get single comments first'
        comment = Comment.objects.get(comment_text="comment1")
        self.assertIsNotNone(comment, "Found 0 comments")
        self.assertIsNotNone(comment.pub_date)

        user1 = User.objects.get(username="user1",password='top_secret')
        author1 = Author.objects.get(user=user1)
        post1 = Post.objects.filter(title="title1")[0]

        self.assertEquals(comment.author, author1, "authors did not match")
        self.assertEquals(comment.post, post1, "posts did not match")
        self.assertEquals(comment.comment_text, "comment1",
                          "comments did not match")

    def testget_all_comments(self):
        """
        getting all comments in the database
        """
        comments = Comment.objects.filter()
        self.assertEqual(len(comments), 3, "3 Comments exist" + 
                 "but only " +  str(len(comments)) + " found")

    def testget_allpost_comments(self):
        """
        retrieving all comments of a specific post from the database
        """
        post2 = Post.objects.filter(title="title2")[0]
            
        comments = Comment.objects.filter(post=post2)
        self.assertEqual(len(comments), 1, "Post has one comment," + 
                 "but " +  str(len(comments)) + " were found")
    

    def test_Other_Author_CanComment(self):
        """
        Tests to see whether other authors can comment
        """
    	post = Post.objects.get(title="title1")
        self.assertIsNotNone(post, "a post exists")
        user6 = User.objects.create_user(username="user6",password="top_secret")

        author6 = Author.objects.create(user=user6)

        comment1=Comment.objects.create(author=author6,post=post,comment_text="comment4")
        comments = Comment.objects.filter(comment_text="comment4")
        self.assertEquals(len(comments), 1, "Comment from other author did not appear")
    
    

