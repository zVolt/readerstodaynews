from django.conf.urls import url
from . import views

urlpatterns = [
    url('post/list', views.PostListView.as_view()),
    url('post/get', views.PostView.as_view()),
    url('tag/list', views.TagListView.as_view()),
]
