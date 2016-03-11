from rest_framework import serializers
from posts.models import Post
from comments.models import Comment
from authors.serializers import AuthorSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    id = serializers.SerializerMethodField('get_comment_id')
    comment = serializers.SerializerMethodField('get_comment_text')
    published = serializers.SerializerMethodField('get_pub_date')

    def get_comment_id(self, obj):
        return obj.comment_id

    def get_comment_text(self, obj):
        return obj.comment_text

    def get_pub_date(self, obj):
        return obj.pub_date

    class Meta:
        model = Comment
        fields = ('author','comment','contentType','id','published')
