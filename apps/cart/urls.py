from django.urls import path

from .views import add_to_cart_view, user_cart_view

urlpatterns = [
    path("product/<int:pk>/add_to_cart/", add_to_cart_view, name="add_to_cart"),
    path("my_cart/", user_cart_view, name="my_cart"),
    path("my_cart/<int:pk>/", user_cart_view, name="cart_element"),
]
