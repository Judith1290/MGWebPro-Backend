from django.urls import include, path

from .router import router_post

urlpatterns = [path("", include(router_post.urls))]
from .views import (
    login_view,
    logout_view,
    products_categories_view,
    products_models_view,
    products_view,
    register_view,
    user_view,
    send_email
)

urlpatterns = [
    path("user/register/", register_view, name="register"),
    path("user/login/", login_view, name="login"),
    path("user/logout/", logout_view, name="logout"),
    path("user/details/", user_view, name="details"),
    path("user/send_email/", send_email, name="send_email"),
    path("product/", products_view, name="products"),
    path("product/<int:pk>/", products_view, name="product"),
    path("product/model/", products_models_view, name="models"),
    path("product/model/<int:pk>/", products_models_view, name="model"),
    path("product/category/", products_categories_view, name="categories"),
    path("product/category/<int:pk>/", products_categories_view, name="category"),
]
