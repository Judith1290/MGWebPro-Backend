from django.urls import include, path

from .router import router_post

urlpatterns = [path("", include(router_post.urls))]
