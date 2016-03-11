from django.conf.urls import url
from . import views
urlpatterns = [
	url(r'^new/', views.comment_new, name='comment_new'),
]
