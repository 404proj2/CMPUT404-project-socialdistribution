from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    #url(r'^$', 'author	s.views.user_login', name='login'),
    #url(r'^$', include('stream.urls',namespace='stream')),
    url(r'^$',include('stream.urls',namespace='stream')),
    url(r'^login/','authors.views.user_login', name='login'),
    url(r'^register/', 'authors.views.register', name='register'),
    url(r'^logout/', 'authors.views.logout', name='logout'),
    url(r'^friends/',include('friends.urls',namespace='friends')),
    url(r'^settings/', 'settings.views.index', name='settings'),
    url(r'^profile/', 'posts.views.show_posts', name='show_posts'),
    url(r'^posts/', include('posts.urls', namespace='posts')),
    url(r'^nodes/', include('nodes.urls', namespace='nodes')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/',include('api.urls',namespace='api')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
]
