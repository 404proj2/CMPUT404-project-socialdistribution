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
        comments = Comment.objects.filter(post=obj.post_id).order_by('-pub_date')
        #comments = Comment.objects.all()
        print comments
        commentSerializer = CommentSerializer(comments, many=True)
        return commentSerializer.data

    def get_post_id(self, obj):
        return obj.post_id

    class Meta:
        model = Post
        fields = ('comments', 'title', 'source', 'origin', 'description', 'contentType', 'content', 'author', 'published', 'id', 'visibility')

class CommentDeserializer(serializers.Serializer):
    author = AuthorSerializer(read_only=True)
    id = serializers.CharField(max_length=200, required=False)
    comment = serializers.CharField(max_length=200, required=False)
    published = serializers.CharField(max_length=200, required=False)

class PostDeserializer(serializers.Serializer):
    author = AuthorSerializer(read_only=True)
    id = serializers.CharField(max_length=200, required=False)
    comments = CommentDeserializer(many=True)

class PostsDeserializer(serializers.Serializer):
    count = serializers.CharField(max_length=200, required=False)
    posts = PostDeserializer()
    #next = serializers.CharField(max_length=200, required=False)
    query = serializers.CharField(max_length=200, required=False)
    size = serializers.CharField(max_length=200, required=False)
    #previous = serializers.CharField(max_length=200, required=False)



