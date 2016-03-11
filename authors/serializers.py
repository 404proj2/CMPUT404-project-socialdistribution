from rest_framework import serializers
from authors.models import Author

class AuthorSerializer(serializers.ModelSerializer):
	displayName = serializers.SerializerMethodField('get_username')
	id = serializers.SerializerMethodField('get_author_id')

	def get_username(self, obj):
		return obj.user.username

	def get_author_id(self, obj):
		return obj.author_id

	class Meta:
		model = Author
		fields = ('id','host','displayName','url', 'github')