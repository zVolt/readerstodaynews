
from django.http import HttpResponse
from django.conf import settings
import os
from django.template.loader import get_template
# Create your views here.

def index(request, name='index'):
    template = get_template('index.html')
    return HttpResponse(template.render())

def about(request, name='about'):
    template = get_template('about.html')
    return HttpResponse(template.render())

def categories(request, name='categories'):
    template = get_template('categories.html')
    return HttpResponse(template.render())

def category(request, name=None):
    template = get_template('category.html')
    data = dict(name=name)
    return HttpResponse(template.render(data))

def post(request, postid=None):
    template = get_template('post.html')
    data = dict(postid=int(postid))
    return HttpResponse(template.render(data))