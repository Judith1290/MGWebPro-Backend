from django.urls import include, path

from .views import generate_imagekit_auth

urlpatterns = [
    path("users/", include("apps.users.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("cart/", include("apps.cart.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("payments/", include("apps.payments.urls")),
    path("imagekit-auth/", generate_imagekit_auth, name="imagekit_auth"),
]
