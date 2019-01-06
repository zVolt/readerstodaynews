# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from .models import Post, Tag, UserProfile, Comment, MenuItem
from django.contrib.auth.models import User
from .serializers import PostDetailSerializer, PostSerializer, TagSerializer, CommentSerializer, MenuSerializer
from reprlib import repr
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
import re

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from firebase_admin import auth
from rest_framework import authentication, permissions
import json


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        id_token = request.data.get('token')
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        auth_user = auth.get_user(uid)
        name, email, photo_url = auth_user.display_name, auth_user.email, auth_user.photo_url
        user = User.objects.filter(email=email).first()
        user_profile = UserProfile.objects.filter(user=user).first() if user else None
        res = {}
        if not user_profile:
            username = email.split('@')[0]
            user = User.objects.create(username=username, first_name=name, email=email, password='')
            user.save()
            user_profile = UserProfile(user=user, profile_pic=photo_url)
            user_profile.save()
        if user and user_profile:
            token, created = Token.objects.get_or_create(user=user_profile.user)
            res['user_id'] = user_profile.pk
            res['email'] = user_profile.user.email
            res['username'] = user_profile.user.username
            res['name'] = user_profile.user.get_full_name()
            res['photo_url'] = user_profile.profile_pic
            res['token'] = token.key
        return Response(res)

class MenuItemListView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer

class TagListView(ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    
    def post(self, request, format=None):
        tags = []
        data = JSONParser().parse(request)
        serializer = TagSerializer(data=data, many=True)
        if serializer.is_valid():
            tags = serializer.save()
        else:
            print(serializer.errors)
        return Response(tags)

class PostListView(ListAPIView):
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        detailed = self.request.query_params.get('detailed', 'false')
        detailed = detailed.strip().lower() == 'true'
        if detailed:
            return PostDetailSerializer
        return PostSerializer

    def get_queryset(self):
        tags = self.request.query_params.get('tags', '')
        sources = self.request.query_params.get('sources', '')
        ids = self.request.query_params.get('ids', '')

        query = Post.objects.all()
        if tags:
            tags = re.split(r'[\s,]+', tags)
            tag_ids = [t.id for t in Tag.objects.filter(name__in=tags)]
            query = query.filter(tags__in=tag_ids)
        
        if sources:
            sources = re.split(r'[\s,]+', sources)
            source_ids = [s.id for s in Source.objects.filter(name__in=sources)]
            query = query.filter(source__in=source_ids)

        if ids:
            ids = [int(_id) for _id in re.split(r'[\s,]+', ids)]
            query = query.filter(id__in=ids)

        return query.order_by('-last_modified_on').all()

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
            posts = []
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        """ List all posts. """
        if request.method == 'GET':
            posts = Post.objects.all()
            serializer = self.serializer_class(posts, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == 'POST':
            data = JSONParser().parse(request)
            serializer = self.serializer_class(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201, safe=False)
            print(serializer.errors)
            return JsonResponse({}, status=400)

class CommentCreateView(CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        data = request.body
        res = {}
        if not data:
            res['status'] = False
            res['details'] = 'no post data'
            return Response(res)
        data = json.loads(data)
        user_profile = UserProfile.objects.filter(user=request.user).first()
        post_id = data.get('post_id')
        post = Post.objects.get(pk=int(post_id))
        res = {}
        if post and user_profile:
            comment = Comment.objects.create(content=data.get('content'), user=user_profile)
            comment.save()
            post.comments.add(comment)
            post.save()
            res['status'] = True
            res.update(dict(comment=CommentSerializer(comment).data))
        else:
            res['status'] = False
            res['details'] = 'no post or user_profile'
        return Response(res)

class LikeCreateView(CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data
        res = {}
        if not data:
            res['status'] = False
            res['details'] = 'no post data'
            return Response(res)
        user_profile = UserProfile.objects.filter(user=request.user).first()
        post_id = data.get('post_id')
        post = Post.objects.get(pk=int(post_id))
        res = {}
        if post and user_profile:
            if user_profile in post.likes.all():
                post.likes.remove(user_profile)
            else:
                post.likes.add(user_profile)
            post.save()
            res['status'] = True
            res.update(dict(like=user_profile in post.likes.all(),
                               likes_count=post.likes.count()))
        return Response(res)