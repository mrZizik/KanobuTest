#coding: utf-8
from django.conf.urls import patterns, url

from rating.views import ArticleListView, ArticleDetailView, like, dislike, post_comment
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^$', ArticleListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', ArticleDetailView.as_view(), name='detail'),
    url(r'^like/(?P<object_id>\d+)/$', like, name="like"),
    url(r'^dislike/(?P<object_id>\d+)/$', dislike, name="dislike"),
    url(r'^comment/(?P<article_id>\d+)/$', post_comment, name="post_comment"),
    url(r'^comment/(?P<article_id>\d+)/(?P<parent_id>\d+)/$', post_comment, name="post_comment"),
    url(r'^accounts/login/$',  login, {'template_name': 'rating/login.html'}, name='login'),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name='logout'),
)