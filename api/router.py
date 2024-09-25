from rest_framework.routers import DefaultRouter

from .views import UsuarioViewSet

router_post = DefaultRouter()
router_post.register(prefix="users", basename="users", viewset=UsuarioViewSet)
