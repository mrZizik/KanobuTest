#coding: utf-8
from django.conf.urls import patterns, url

from rating.views import ArticleListView, ArticleDetailView

urlpatterns = patterns('',
    url(r'^$', ArticleListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', ArticleDetailView.as_view()),
)