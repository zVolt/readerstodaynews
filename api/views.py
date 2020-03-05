# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated

from firebase_admin import auth

from reprlib import repr
import re
import json

from .models import Post, Category, UserProfile, Comment, MenuItem, Source
from .serializers import (
    PostDetailSerializer,
    PostSerializer,
    CategorySerializer,
    CommentSerializer,
    MenuSerializer,
    CounterSerializer,
)
from .permissions import ReadOnly


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        id_token = request.data.get("token")
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token["uid"]
        auth_user = auth.get_user(uid)
        name, email, photo_url = (
            auth_user.display_name,
            auth_user.email,
            auth_user.photo_url,
        )
        user = User.objects.filter(email=email).first()
        user_profile = UserProfile.objects.filter(user=user).first() if user else None
        res = {}
        if not user_profile:
            username = email.split("@")[0]
            user = User.objects.create(
                username=username, first_name=name, email=email, password=""
            )
            user.save()
            user_profile = UserProfile(user=user, profile_pic=photo_url)
            user_profile.save()
        if user and user_profile:
            token, created = Token.objects.get_or_create(user=user_profile.user)
            res["user_id"] = user_profile.pk
            res["email"] = user_profile.user.email
            res["username"] = user_profile.user.username
            res["name"] = user_profile.user.get_full_name()
            res["photo_url"] = user_profile.profile_pic
            res["token"] = token.key
        return Response(res)


class MenuItemListView(ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)


class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True
        return super().get_serializer(*args, **kwargs)


class PostListView(ListAPIView):
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticated | ReadOnly]

    def get_serializer_class(self):
        detailed = self.request.query_params.get("detailed", "false")
        detailed = detailed.strip().lower() == "true"
        if detailed:
            return PostDetailSerializer
        return PostSerializer

    def get_queryset(self):
        categories = self.request.query_params.get("categories", "")
        sources = self.request.query_params.get("sources", "")
        ids = self.request.query_params.get("ids", "")

        query = Post.objects.all()
        if categories:
            categories = re.split(r"[\s,]+", categories)
            category_ids = [t.id for t in Category.objects.filter(name__in=categories)]
            query = query.filter(categories__in=category_ids)

        if sources:
            sources = re.split(r"[\s,]+", sources)
            source_ids = [s.id for s in Source.objects.filter(name__in=sources)]
            query = query.filter(source__in=source_ids)

        if ids:
            ids = [int(_id) for _id in re.split(r"[\s,]+", ids)]
            query = query.filter(id__in=ids)

        return query.order_by("-last_modified_on").all()


class SingleResultsSetPagination(LimitOffsetPagination):
    default_limit = 3


class PostView(APIView):
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, format=None):
        ids = request.query_params.get("ids", "")
        post = []
        if ids:
            ids = [int(_id) for _id in re.split(r"[\s,]+", ids)]
            posts = Post.objects.filter(id__in=ids).all()
        else:
            posts = []
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        """ List all posts. """
        if request.method == "GET":
            posts = Post.objects.all()
            serializer = self.serializer_class(posts, many=True)
            return JsonResponse(serializer.data, safe=False)
        elif request.method == "POST":
            data = JSONParser().parse(request)
            serializer = self.serializer_class(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201, safe=False)
            print(serializer.errors)
            return JsonResponse({}, status=400)


class CommentCreateView(CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [IsAuthenticated | ReadOnly]

    def post(self, request, format=None):
        data = request.body
        res = {}
        if not data:
            res["status"] = False
            res["details"] = "no post data"
            return Response(res)
        data = json.loads(data)
        user_profile = UserProfile.objects.filter(user=request.user).first()
        post_id = data.get("post_id")
        post = Post.objects.get(pk=int(post_id))
        res = {}
        if post and user_profile:
            comment = Comment.objects.create(
                content=data.get("content"), user=user_profile
            )
            comment.save()
            post.comments.add(comment)
            post.save()
            res["status"] = True
            res.update(dict(comment=CommentSerializer(comment).data))
        else:
            res["status"] = False
            res["details"] = "no post or user_profile"
        return Response(res)


class LikeCreateView(CreateAPIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [IsAuthenticated | ReadOnly]

    def post(self, request, format=None):
        data = request.data
        res = {}
        if not data:
            res["status"] = False
            res["details"] = "no post data"
            return Response(res)
        user_profile = UserProfile.objects.filter(user=request.user).first()
        post_id = data.get("post_id")
        post = Post.objects.get(pk=int(post_id))
        res = {}
        if post and user_profile:
            if user_profile in post.likes.all():
                post.likes.remove(user_profile)
            else:
                post.likes.add(user_profile)
            post.save()
            res["status"] = True
            res.update(
                dict(
                    like=user_profile in post.likes.all(),
                    likes_count=post.likes.count(),
                )
            )
        return Response(res)


class CounterListAPIView(ListAPIView):
    serializer_class = CounterSerializer
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        print(object)
        return super().get(request, *args, **kwargs)
