import uuid

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..api.authentication import CookieAuthentication
from ..cart.models import Carrito
from ..inventory.models import Producto
from .models import Pago
from .serializers import PagoSerializer


@api_view(["GET"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def user_payments_view(request):
    instance = Pago.objects.filter(user_id=request.user.user_id)
    serializer = PagoSerializer(instance=instance, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def stripe_checkout_view(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    product = get_object_or_404(Producto, producto_id=request.data["producto_id"])
    if (product.stock - request.data["cantidad"]) < 0 or not product.is_active:
        return Response(
            {"detail": "There is not enough stock or the product is not available."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "crc",
                        "unit_amount": product.precio * 100,
                        "product_data": {
                            "name": product.nombre,
                            "description": product.descripcion,
                            "images": [product.imagen],
                        },
                    },
                    "quantity": request.data["cantidad"],
                },
            ],
            metadata={
                "user_id": str(request.user.user_id),
                "product_id": product.producto_id,
                "quantity": request.data["cantidad"],
                "cart_id": request.data["carrito_id"]
                if "carrito_id" in request.data
                else "",
            },
            mode="payment",
            success_url="http://localhost:5173/" + "?success=true",
            cancel_url="http://localhost:5173/" + "?canceled=true",
        )
    except Exception:
        return Response(
            {"detail": "Something went wrong when creating stripe checkout session"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return redirect(checkout_session.url)


@csrf_exempt
@api_view(["POST"])
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        metadata = session["metadata"]

        if metadata["cart_id"]:
            cart = get_object_or_404(Carrito, carrito_id=int(metadata["cart_id"]))
            cart.delete()

        data = {
            "user": uuid.UUID(metadata["user_id"]),
            "stripe_checkout_id": session["payment_intent"],
            "cantidad": int(metadata["quantity"]),
        }
        serializer = PagoSerializer(data=data)
        if serializer.is_valid():
            serializer.save(producto_id=int(metadata["product_id"]))

        product = get_object_or_404(Producto, producto_id=metadata["product_id"])
        product.stock = product.stock - int(metadata["quantity"])
        product.save()

    return Response(status=status.HTTP_200_OK)
