import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_dist.settings')

import django
django.setup()

from authors.models import Author, User, GlobalAuthor, LocalRelation, GlobalRelation

def populate():
	author1 = add_local_user('TestPop1') # will make it local --- main user I want to log in as via UI to see if this worked.
	author2 = add_local_user('TestPop2') # will make it local
	author3 = add_local_user('TestPop3') # will make it local
	author4 = add_global_author('TestPop4') # will make it global
	author5 = add_global_author('TestPop5') # will make it global

	# Create relationships:
	add_local_relationship(author1, author2, True) # status=True to be friends locally.
	add_local_relationship(author1, author3, True)
	add_global_relationship(author1, author4, 2) # status=2 to be friends globally.
	add_global_relationship(author1, author5, 2) # status=2 to be friends globally.


def add_local_user(username):
	user_test = User.objects.create(username=username, password='populate')
	user_test.save()

	author_test = Author.objects.create(user=user_test)

	return author_test

def add_global_author(username, host='notthelocalone'):
	global_author_test = GlobalAuthor.objects.create(global_author_name=username, host=host)

	return global_author_test

def add_local_relationship(first_author, second_author, status):
	local_relation = LocalRelation.objects.create(author1=first_author, author2=second_author, relation_status=status)

def add_global_relationship(first_author, second_author, status):
	global_relation = GlobalRelation.objects.create(local_author=first_author, global_author=second_author, relation_status=status)

# Source: http://www.tangowithdjango.com/book17/chapters/models.html#creating-a-population-script 2016-03-06
if __name__ == '__main__':
    print "Starting Social Distribution population script..."
    populate()