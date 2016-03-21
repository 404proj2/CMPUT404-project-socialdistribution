from django.contrib import admin
from .models import Comment, GlobalComment
admin.site.register(Comment, GlobalComment)
