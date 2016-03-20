from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
#[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12} taken from http://stackoverflow.com/questions/136505/searching-for-uuids-in-text-with-regex
urlpatterns = [
	url(r'^$', views.index, name='test'),

	url(r'^friends/(?P<uuid1>[0-9a-z-]+)/(?P<uuid2>[0-9a-z-]+)', views.queryFriend2Friend, name='queryFriend2Friend'),
	url(r'^friends/(?P<uuid>[0-9a-z-]+)', views.queryFriends, name='queryFriends'),
	url(r'^author/posts', views.getPosts, name='getPosts'),
	url(r'^author/(?P<uuid>[0-9a-z-]+)/posts', views.authorPost, name='authorPost'),
	url(r'^author/(?P<uuid>[0-9a-z-]+)', views.getProfile, name='getProfile'),
	url(r'^posts/(?P<uuid>[0-9a-z-]+)/comments', views.comments, name='comments'),
	url(r'^posts/(?P<uuid>[0-9a-z-]+)', views.singlePost, name='singlePost'),
	url(r'^posts', views.publicPosts, name='publicPosts'),
	url(r'^friendrequest', views.friendRequest, name='friendRequest'),
	url(r'^authors', views.allAuthors, name='allAuthors'),
]