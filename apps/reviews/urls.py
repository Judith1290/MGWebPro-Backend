from django.urls import path

from .views import reviews_view

urlpatterns = [
    path("product/<int:product_id>/", reviews_view, name="reviews"),
    path("product/<int:product_id>/comment/<int:review_id>/", reviews_view, name="specific_review")
]