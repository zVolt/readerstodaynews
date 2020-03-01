from django.urls import path
from . import views

app_name = "frontend"
urlpatterns = [
    path("", views.index, name="index"),
    path("index", views.index, name="index"),
    path("about", views.about, name="about"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:name>", views.category, name="category"),
    path("post/<int:postid>", views.post, name="post"),
]
