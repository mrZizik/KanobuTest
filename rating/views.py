from .models import Article, Rate, Comment
from django.views.generic import ListView, DetailView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template.defaulttags import register
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template import RequestContext
from .forms import CommentForm
import json


class ArticleListView(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        article = context['article']
        comment_ratings = {}
        for comment in article.comments.all():
            rate = {}
            rate["likes"] = comment.rates.filter(side=1).count()
            rate["dislikes"] = comment.rates.filter(side=-1).count()
            rate["rating"] = comment.rates.count()
            comment_ratings[comment.id] = rate
        context['comment_ratings'] = comment_ratings
        context['article_rating'] = article.rates.count()
        context['article_likes'] = article.rates.filter(side=1).count()
        context['article_dislikes'] = article.rates.filter(side=-1).count()
        return context


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/account/loggedout/")


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        auth.login(request, user)
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/account/invalid/")


def check_rate_exist(user, material):
    try:
        rate = material.rates.get(user=user)
        return rate
    except Rate.DoesNotExist:
        return False


@transaction.atomic
@login_required
def like(request, object_id):
    material_type = request.POST.get("type")
    material = None
    try:
        if material_type == "comment":
            material = Comment.objects.get(id=object_id)
        elif material_type == "article":
            material = Article.objects.get(id=object_id)
        rate = check_rate_exist(request.user, material)
        if rate:
            if rate.side == 1:
                rate.delete()
            else:
                rate.side = 1
                rate.save()
        else:

            rate = Rate.objects.get_or_create(user=request.user, object_id=material.id,
                                              content_type=ContentType.objects.get_for_model(material), side=1)
        response = {}
        response["likes"] = material.rates.filter(side=1).count()
        response["dislikes"] = material.rates.filter(side=-1).count()
        response["summ"] = material.rates.count()
        return HttpResponse(json.dumps(response))
    except ObjectDoesNotExist:
        return HttpResponseNotFound()


@transaction.atomic
@login_required
def dislike(request, object_id):
    material_type = request.POST.get("type")
    material = None
    try:
        if material_type == "comment":
            material = Comment.objects.get(id=object_id)
        elif material_type == "article":
            material = Article.objects.get(id=object_id)
        rate = check_rate_exist(request.user, material)
        if rate:
            if rate.side == -1:
                rate.delete()
            else:
                rate.side = -1
                rate.save()
        else:
            rate = Rate.objects.get_or_create(user=request.user, object_id=material.id,
                                              content_type=ContentType.objects.get_for_model(material), side=-1)
        response = {}
        response["likes"] = material.rates.filter(side=1).count()
        response["dislikes"] = material.rates.filter(side=-1).count()
        response["summ"] = material.rates.count()
        return HttpResponse(json.dumps(response))
    except ObjectDoesNotExist:
        return HttpResponseNotFound()


@transaction.atomic
@login_required
def post_comment(request, article_id, parent_id=None):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                article = Article.objects.get(id=article_id)
            except ObjectDoesNotExist:
                return HttpResponseNotFound("Not found")
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article_id = article_id
            if request.POST.get("parent_id"):
                try:
                    parent_comment = Comment.objects.get(id=request.POST.get("parent_id"))
                except ObjectDoesNotExist:
                    return HttpResponseNotFound("Not found")
                comment.parent = parent_comment
            comment.save()
            return HttpResponseRedirect('/'+article_id)
        else:
            return render(request, 'rating/comment_form.html', locals(), context_instance=RequestContext(request))
    form = CommentForm()
    ctx = {'form': form, 'article_id': article_id}
    if parent_id:
        ctx["parent_id"] = parent_id
    return render(request, 'rating/comment_form.html', ctx)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)