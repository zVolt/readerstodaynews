from django.http import HttpResponse
from django.conf import settings
import os
from django.template.loader import get_template
import random

random.seed(0)


def get_count():
    return 0
    counter = Counter.objects.first()
    if counter is None:
        counter = Counter.objects.create()
    new_count = int(counter.counter) + random.randint(1, 10)
    counter.counter = str(new_count)
    counter.save()
    return counter.counter


def index(request, name="index"):
    template = get_template("index.html")
    return HttpResponse(template.render(dict(counter=get_count())))


def about(request, name="about"):
    template = get_template("about.html")
    return HttpResponse(template.render(dict(counter=get_count())))


def categories(request, name="categories"):
    template = get_template("categories.html")
    return HttpResponse(template.render(dict(counter=get_count())))


def category(request, name=None):
    template = get_template("category.html")
    data = dict(name=name, counter=get_count())
    return HttpResponse(template.render(data))


def post(request, postid=None):
    template = get_template("post.html")
    data = dict(postid=int(postid), counter=get_count())
    return HttpResponse(template.render(data))
