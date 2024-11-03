from django.urls import path

from .views import stripe_checkout_view, stripe_webhook, user_payments_view

urlpatterns = [
    path("create_checkout_session/", stripe_checkout_view, name="checkout"),
    path("webhooks/stripe/", stripe_webhook, name="stripe_webhook"),
    path("my_payments/", user_payments_view, name="user_payments"),
]
