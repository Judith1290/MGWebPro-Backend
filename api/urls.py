from django.urls import path

from .views import (
    add_to_cart_view,
    login_view,
    logout_view,
    products_categories_view,
    products_models_view,
    products_view,
    register_view,
    reviews_view,
    user_cart_view,
    user_view,
)

urlpatterns = [
    path("user/register/", register_view, name="register"),
    path("user/login/", login_view, name="login"),
    path("user/logout/", logout_view, name="logout"),
    path("user/details/", user_view, name="details"),
    path("user/cart/", user_cart_view, name="cart"),
    path("user/cart/<int:pk>/", user_cart_view, name="cart"),
    path("product/", products_view, name="products"),
    path("product/<int:pk>/add_to_cart/", add_to_cart_view, name="add_to_cart"),
    path("product/<int:pk>/", products_view, name="product"),
    path("product/<int:product_id>/review/", reviews_view, name="reviews"),
    path("product/<int:product_id>/review/<int:review_id>/", reviews_view, name="review"),
    path("model/", products_models_view, name="models"),
    path("model/<int:pk>/", products_models_view, name="model"),
    path("category/", products_categories_view, name="categories"),
    path("category/<int:pk>/", products_categories_view, name="category"),
]
