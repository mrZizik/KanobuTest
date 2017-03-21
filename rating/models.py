"""
Ali Abdulmadzhidov
14.03.17 21:00
"""

from django.db import models
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation


class Rate(models.Model):
    side = models.SmallIntegerField(null=False, blank=False)
    user = models.ForeignKey(User, related_name="rates_posted", null=False, blank=False)

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Article(models.Model):
    title = models.CharField(max_length=144, null=False, blank=False)
    text = models.TextField(null=False, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updateAt = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=False, blank=False,related_name="articles")
    rates = GenericRelation(Rate)

    def get_absolute_url(self):
        return "/{}/".format(self.id)

    def __unicode__(self):
        return self.title


class Comment(MPTTModel):
    text = models.TextField(null=False, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='comments', null=False, blank=False)
    article = models.ForeignKey(Article, related_name='comments', null=False, blank=False)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    rates = GenericRelation(Rate)

    def __unicode__(self):
        return self.text

    class MPTTMeta:
        order_insertion_by = ['createdAt']



