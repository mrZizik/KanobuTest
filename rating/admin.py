from django.contrib import admin
from rating.models import Article, Comment, Rate

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Rate)

