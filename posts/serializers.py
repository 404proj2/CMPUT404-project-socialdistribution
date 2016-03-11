from rest_framework import serializers
from posts.models import Post
from comments.models import Comment
from authors.serializers import AuthorSerializer
from comments.serializers import CommentSerializer

class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    id = serializers.SerializerMethodField('get_post_id')
    comments = serializers.SerializerMethodField('get_post_comments') 

    def get_post_comments(self, obj):
        comments = Comment.objects.filter(post=obj.post_id)
        #comments = Comment.objects.all()
        print comments
        commentSerializer = CommentSerializer(comments, many=True)
        return commentSerializer.data

    def get_post_id(self, obj):
        return obj.post_id

    class Meta:
        model = Post
        fields = ('comments', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'published', 'id', 'visibility')