from django.urls import path
from . import views
from rest_framework.routers import SimpleRouter

app_name = "api"

router = SimpleRouter()
router.register(r"menu", views.MenuViewSet, basename="menu")
router.register(r"category", views.CategoryViewSet, basename="category")
router.register(r"counter", views.CounterViewSet, basename="counter")
router.register(r"source", views.SourceViewSet, basename="source")
router.register(r"post", views.PostViewSet, basename="post")


urlpatterns = [
    path("auth/", views.CustomAuthToken.as_view()),
]
urlpatterns += router.urls
