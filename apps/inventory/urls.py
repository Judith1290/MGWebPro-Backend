from django.urls import path

from .views import (
    change_product_status_view,
    products_categories_view,
    products_models_view,
    products_view,
)

urlpatterns = [
    path("products/", products_view, name="products"),
    path("products/<int:pk>/", products_view, name="specific_product"),
    path("categories/", products_categories_view, name="categories"),
    path("categories/<int:pk>/", products_categories_view, name="specific_category"),
    path("models/", products_models_view, name="models"),
    path("models/<int:pk>/", products_models_view, name="specific_model"),
    path("products/<int:pk>/change_status/", change_product_status_view, name="change_status")
]

