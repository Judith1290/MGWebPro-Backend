from django.urls import path

from .views import (
    generate_imagekit_auth,
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
    # temporal: luego lo moveré a un lugar más adecuado
    path("imagekit-auth/", generate_imagekit_auth, name="imagekit_auth"),
]
