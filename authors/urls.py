from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^home/', views.index, name='home'),
	url(r'^profile/', views.view_user_profile, name='profile'),
]