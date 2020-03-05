from rest_framework import serializers
from .models import (
    Counter,
    UserProfile,
    MenuItem,
    Category,
    MediaType,
    Source,
    Media,
    Comment,
    PostType,
    Post,
    BaseUser,
)
import cloudinary


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = UserProfile
        fields = ("username", "profile_pic", "id")
        validators = []


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ("name", "id", "url", "menu", "order")

    def create(self, validated_data):
        request = self.context.get("request")
        return MenuItem.objects.create(
            last_modified_by_id=request.user.id, **validated_data
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "id", "image")

    def to_representation(self, instance):
        representation = super(CategorySerializer, self).to_representation(instance)
        if instance.image:
            representation["image"] = instance.image.url
        return representation


class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = ("name", "id")


class SourceSerializer(serializers.ModelSerializer):
    follower_count = serializers.SerializerMethodField(read_only=True)

    def get_follower_count(self, obj):
        return obj.followers.count()

    class Meta:
        model = Source
        fields = ("name", "icon", "follower_count", "id")

    def to_representation(self, instance):
        representation = super(SourceSerializer, self).to_representation(instance)
        if instance.icon:
            representation["icon"] = instance.icon.url
        return representation


class MediaSerializer(serializers.ModelSerializer):
    media_type = MediaTypeSerializer()

    class Meta:
        model = Media
        fields = ("media_type", "image", "video_url", "title", "id")
        validators = []

    def to_representation(self, instance):
        representation = super(MediaSerializer, self).to_representation(instance)
        if instance.image:
            representation["image"] = instance.image.url
        return representation


class CommentSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ("content", "user", "last_modified_on", "id")


class PostTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostType
        fields = ("name", "id")


class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    media_items = MediaSerializer(many=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    comments_count = serializers.SerializerMethodField(read_only=True)
    source = SourceSerializer(read_only=True)
    post_type = PostTypeSerializer()

    def get_likes_count(self, post):
        return post.likes.count()

    def get_comments_count(self, post):
        return post.comments.count()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "summary",
            "source",
            "categories",
            "media_items",
            "last_modified_on",
            "likes_count",
            "comments_count",
            "post_type",
            "share_count",
        )
        validators = []


class PostDetailSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    media_items = MediaSerializer(many=True)
    comments = CommentSerializer(many=True)
    likes = UserProfileSerializer(many=True)
    source = SourceSerializer()
    post_type = PostTypeSerializer()

    class Meta:
        model = Post
        fields = (
            "id",
            "title",
            "summary",
            "source",
            "content",
            "categories",
            "media_items",
            "last_modified_on",
            "likes",
            "comments",
            "share_count",
            "post_type",
        )

    def create(self, validated_data):
        # Categorys
        categories_data = validated_data.pop("categories")
        categories_names = [td.get("name") for td in categories_data]
        categories = Category.objects.filter(name__in=categories_names)
        # Modified by
        user = BaseUser.objects.get(pk=1)

        # Media Items
        media_data = validated_data.pop("media_items")
        media_items = []
        for md in media_data:
            media_type_name = md.pop("media_type").get("name")
            mt = MediaType.objects.filter(name=media_type_name).first()
            media = Media.objects.create(last_modified_by=user, media_type=mt, **md)
            media.save()
            media_items.append(media)
        validated_data.pop("likes")
        validated_data.pop("comments")
        post_type = validated_data.pop("post_type")
        post_type = PostType.objects.filter(name=post_type.get("name")).first()
        source = validated_data.pop("source")
        source = Source.objects.filter(name=source.get("name")).first()
        post = Post.objects.create(
            post_type=post_type, last_modified_by=user, source=source, **validated_data
        )
        post.categories.set(categories)
        post.media_items.set(media_items)
        return post


class CounterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counter
        fields = (
            "id",
            "type",
            "count",
        )
