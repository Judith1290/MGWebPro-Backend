from django.urls import re_path

from .views import login_view, logout_view, register_view, user_view

urlpatterns = [
    re_path(route="user/register", view=register_view),
    re_path(route="user/login", view=login_view),
    re_path(route="user/logout", view=logout_view),
    re_path(route="user/details", view=user_view),
]
