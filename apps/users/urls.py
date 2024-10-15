from django.urls import path

from .views import login_view, logout_view, register_view, user_view

# Urls relacionadas al usuario
# ¿hace falta documentar esto?
urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("my_details/", user_view, name="details"),
]
