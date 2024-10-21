from django.urls import include, path

from .views import generate_imagekit_auth
from .views import enviar_correo

urlpatterns = [
    path("users/", include("apps.users.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("cart/", include("apps.cart.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("imagekit-auth/", generate_imagekit_auth, name="imagekit_auth"),
    path("enviar-correo/", enviar_correo, name='enviar_correo'),
]
