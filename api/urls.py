from django.conf.urls import url
from . import views

urlpatterns = [
    url("auth/", views.CustomAuthToken.as_view()),

    url("post/list", views.PostListView.as_view()),
    url("post/", views.PostView.as_view()),
    url("comment/", views.CommentCreateView.as_view()),
    url("like/", views.LikeCreateView.as_view()),
    url("category/list", views.CategoryListView.as_view()),
    url("menu/<int:pk>", views.MenuItemListView.as_view()),
    url("menu/list$", views.MenuItemListView.as_view(), name='menu-list'),
    url("counter/", views.CounterListAPIView.as_view())
]
