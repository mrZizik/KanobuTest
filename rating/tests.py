#!/usr/bin/env python
from unittest import TestCase
from django.contrib import auth
from django.test import Client
from django.core.urlresolvers import reverse
from rating.models import Article, Comment, Rate
from django.contrib.auth.models import User


__author__ = 'Ali Abdulmadzdhidov'


class TestRating(TestCase):

    def setUp(self):
        self.client = Client()
        self.username = 'agco123nti'
        self.email = 'test@test.com'
        self.password = 'test'
        if not self.client.login(username = self.username, password = self.password):
            self.user = User.objects.create_user(self.username, self.email, self.password)
            self.client.login(username=self.username, password=self.password)
        Article.objects.create(title="some titile", text="some text", author_id=1).save()
        Comment.objects.create(text="some_coment", article_id=1, author_id=1).save()

    def test_index(self):
        response = self.client.get(reverse('list'))
        assert response.status_code == 200

    def test_detail_ok(self):
        response = self.client.get(reverse('detail', kwargs={"pk": 1}))
        assert response.status_code == 200

    def test_detail_not_found(self):
        response = self.client.get(reverse('detail', kwargs={"pk": 2}))
        assert response.status_code == 404

    def test_like(self):
        response = self.client.post(reverse('like', kwargs={"object_id": "2"}), {"type": "article"})
        print response.status_code
        assert response.status_code == 200

    def test_like_not_found(self):
        response = self.client.post(reverse('like', kwargs={"object_id": "100"}), {"type": "article"})
        print response.status_code
        assert response.status_code == 404

    def test_dislike_not_found(self):
        response = self.client.post(reverse('dislike', kwargs={"object_id": "100"}), {"type": "article"})
        print response.status_code
        assert response.status_code == 404
