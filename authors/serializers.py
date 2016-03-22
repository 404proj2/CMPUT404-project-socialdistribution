from rest_framework import serializers
from authors.models import Author, GlobalAuthor
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
	displayName = serializers.SerializerMethodField('get_username')
	id = serializers.SerializerMethodField('get_author_id')

	def get_username(self, obj):
		try:
			return obj.user.username
		except:
			return obj.global_author_name

	def get_author_id(self, obj):
		try:
			return obj.author_id
		except:
			return obj.global_author_id

	class Meta:
		model = Author
		fields = ('id','host','displayName','url', 'github')



class AuthorRequestSerializer(serializers.ModelSerializer):

	displayName = serializers.SerializerMethodField('get_username')
	id = serializers.SerializerMethodField('get_author_id')
	friends = serializers.SerializerMethodField('get_friendses')


	def get_username(self, obj):
		return obj.user.username

	def get_author_id(self, obj):
		return obj.author_id

	def get_host(self,obj):
		return obj.host

	def get_url(self,obj):
		host = obj.host
		auth_id = obj.obj.author_id
		filler = 'author/'
		final_string = host+filler+auth_id
		return final_string

	def get_friendses(self, obj):
		local_relations = obj.getLocalFriends()
		global_relations = obj.getGlobalFriends()
		all_relations = local_relations + global_relations
		#all_relations = Author.objects.all()
		print all_relations
		friend_serializer = FriendSerializer(all_relations, many=True)
		print "this shit"
		print friend_serializer.data
		

		return friend_serializer.data

	class Meta:
		model = Author
		fields = ('id','host','displayName','url','friends')

class FriendSerializer(serializers.ModelSerializer):
	"""docstring for FriendSerializer"""
	id = serializers.SerializerMethodField('get_author_id')
	displayName = serializers.SerializerMethodField('get_username')

	def get_username(self, obj):
		if obj.getClassName() == "Author":
			return obj.user.username
		elif obj.getClassName() == "GlobalAuthor":
			return obj.global_author_name

	def get_author_id(self, obj):
		if obj.getClassName() == "Author":
			return obj.author_id
		elif obj.getClassName() == "GlobalAuthor":
			return obj.global_author_id

	def get_host(self,obj):
		return obj.host

	def get_url(self,obj):
		host = obj.host
		auth_id = obj.obj.author_id
		filler = 'author/'
		final_string = host+filler+auth_id
		return final_string

	class Meta:
		"""docstring for Meta"""
		model = Author
		fields = ('id','host','displayName','url')

