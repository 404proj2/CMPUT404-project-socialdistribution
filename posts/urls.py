from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^$', views.post_new, name='post_new'),
	url(r'^delete/', views.delete_post, name='delete_post'),
	url(r'^images/', views.add_image, name='add_image'),
]