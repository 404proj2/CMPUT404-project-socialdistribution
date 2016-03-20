#from authors.models import Author

class AuthorConverter():
	
	def convert(self, author_dict):
		author = Author()
		
		author.id = author_dict['id']
		author.host = author_dict['host']
		author.displayName = author_dict['displayName']
		author.url = author_dict['url']
		author.github = author_dict['github']
		
		return author

class Author():
	author_id = ""
	url = ""
	host = ""
	profile_pic = ""
	github = ""