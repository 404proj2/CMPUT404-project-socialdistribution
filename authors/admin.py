from django.contrib import admin
from .models import Author, GlobalAuthor, LocalRelation, GlobalRelation
# Register your models here.
admin.site.register(Author)
admin.site.register(GlobalAuthor)
admin.site.register(LocalRelation)
admin.site.register(GlobalRelation)