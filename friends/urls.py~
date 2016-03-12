from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^search/', views.search, name='search'),
	url(r'^delete_local/(?P<author_id>[0-9a-z-]+)/', views.deleteLocalFriend, name='delete_local'),
	url(r'^delete_global/(?P<global_author_id>[0-9a-z-]+)/', views.deleteGlobalFriend, name='delete_global'),
	url(r'^add_local/(?P<author_id>[0-9a-z-]+)/', views.addLocalFriend, name='add_local'),
	url(r'^add_global/(?P<global_author_id>[0-9a-z-]+)/', views.addGlobalFriend, name='add_global'),
]