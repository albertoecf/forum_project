from django.contrib import admin
from app_blog.models import PostModel, CommentModel
# Register your models here.

admin.site.register(PostModel)
admin.site.register(CommentModel)
