from authors.converter import AuthorConverter
from authors.converter import Author

from datetime import datetime

class CommentConverter():
	
	def convert(self, comment_dict):
		authorConv = AuthorConverter()

		comment = Comment()
		
		comment.comment_id = comment_dict['id']
		comment.comment_text = comment_dict['comment']
		comment.contentType = comment_dict['contentType']
		try:
			comment.pub_date = datetime.strptime(comment_dict['published'], "%Y-%m-%dT%H:%M:%S.%fZ")
		except:
			comment.pub_date = datetime.strptime(comment_dict['published'], "%Y-%m-%dT%H:%M:%SZ")
		comment.author = authorConv.convert(comment_dict['author']).displayName
		
		return comment

class Comment():
	author = Author()
	comment_id = ""
	pub_date = ""
	comment_text = ""
	contentType = ""