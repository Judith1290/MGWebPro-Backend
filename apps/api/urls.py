from django.urls import include, path

urlpatterns = [
    path("users/", include("apps.users.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("cart/", include("apps.cart.urls")),
    path("reviews/", include("apps.reviews.urls")),
]
