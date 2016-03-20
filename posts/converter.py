from authors.converter import AuthorConverter
from authors.converter import Author
from comments.converter import CommentConverter
from comments.converter import Comment

from datetime import datetime

class PostConverter():
	
	def convert(self, post_dict):
		commentConv = CommentConverter()
		authorConv = AuthorConverter()

		print post_dict['id']

		post = Post()
		
		post.post_id = post_dict['id']
		post.server = post_dict['server']
		post.title = post_dict['title']
		post.source = post_dict['source']
		post.origin = post_dict['origin']
		post.description = post_dict['description']
		post.contentType = post_dict['contentType']
		post.content = post_dict['content']
		try:
			post.published = datetime.strptime(post_dict['published'], "%Y-%m-%dT%H:%M:%S.%fZ")
		except:
			post.published = datetime.strptime(post_dict['published'], "%Y-%m-%dT%H:%M:%SZ")
		#post.published = datetime.strptime(post_dict['published'], "%Y-%m-%dT%H:%M:%S.%fZ")
		post.visibility = post_dict['visibility']
		post.comments = []
		for comment in post_dict['comments']:
			c = commentConv.convert(comment)
			post.comments.append(c)
		post.author = authorConv.convert(post_dict['author']).displayName

		return post

class Post():
	author = Author()
	post_id = ""
	published = ""
	content = ""
	title = ""
	contentType = ""
	visibility = ""
	source = ""
	origin = ""
	description = ""