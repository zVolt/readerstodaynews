# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from .models import Post, Tag
from .serializers import PostSerializer, PostListSerializer, TagSerializer
from reprlib import repr
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
import re

class TagListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class PostListView(ListAPIView):
    serializer_class = PostListSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        tags = self.request.query_params.get('tags', '')
        if tags:
            tag_names = re.split(r'[\s,]+', tags)
            tag_ids = [t.id for t in Tag.objects.filter(name__in=tag_names)]
            return Post.objects.filter(tags__in=tag_ids).order_by('-last_modified_on').all()
        return Post.objects.order_by('-last_modified_on').all()

class SingleResultsSetPagination(LimitOffsetPagination):
    default_limit = 3

class PostView(APIView):
    serializer_class = PostSerializer

    def get(self, request, format=None):
        ids = request.query_params.get('ids', '')
        post = []
        if ids:
            ids = [int(_id) for _id in re.split(r'[\s,]+', ids)]
            posts = Post.objects.filter(id__in=ids).all()
        else:
            posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

@csrf_exempt
def post_list(request):
    """ List all posts. """
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        print(repr(data))
        print(data[0].keys())
        serializer = PostSerializer(data=data, many=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201, safe=False)
        print(serializer.errors)
        return JsonResponse(serializer.errors, status=400)