import ast

import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from utils.email_utils import send_email
from utils.file_utils import create_pdf

from ..api.authentication import CookieAuthentication
from ..cart.models import Carrito
from ..inventory.models import Producto
from .models import Factura
from .serializers import (
    FacturaSerializer,
)
from .utils import create_invoice, update_products_and_cart_items


@api_view(["GET"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def user_payments_view(request):
    instance = Factura.objects.filter(user_id=request.user.user_id)
    serializer = FacturaSerializer(instance=instance, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@authentication_classes([CookieAuthentication])
@permission_classes([IsAuthenticated])
def stripe_checkout_view(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    global purchase_data
    global line_items

    if request.data:  # pago directo
        product = get_object_or_404(Producto, producto_id=request.data["producto"])
        if not product.is_active:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        purchase_data = [
            {"product_id": product.producto_id, "quantity": request.data["cantidad"]}
        ]
        line_items = [
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
            }
        ]
    else:  # pago de carrito
        # Objetos de carrito que estén relacionados al usuario logeado.
        cart_items = Carrito.objects.filter(user_id=request.user.user_id)
        # Lista con datos para uso logico. No se incluyen productos que tengan un estado de "inactivo".
        purchase_data = [
            {
                "cart_id": item.carrito_id,
                "product_id": item.producto.producto_id,
                "quantity": item.cantidad,
            }
            for item in cart_items
            if item.producto.is_active
        ]
        # Lista con lo datos necesarios para realizar el pago por stripe. No se incluyen productos que tengan un estado de "inactivo".
        line_items = [
            {
                "price_data": {
                    "currency": "crc",
                    "unit_amount": item.producto.precio * 100,
                    "product_data": {
                        "name": item.producto.nombre,
                        "description": item.producto.descripcion,
                        "images": [item.producto.imagen],
                    },
                },
                "quantity": item.cantidad,
            }
            for item in cart_items
            if item.producto.is_active
        ]

    # Antes de realizar la compra se comprueba que haya suficiente stock de los productos solicitados.
    for e in purchase_data:
        product = Producto.objects.get(producto_id=e["product_id"])
        if product.stock - e["quantity"] < 0:
            return Response(
                {
                    "detail": f"{product.nombre} does not have enough stock. ({product.stock} remaining)"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            customer_email=request.user.email,
            metadata={
                "user_id": str(request.user.user_id),
                "purchase_data": str(purchase_data),
            },
            mode="payment",
            success_url="http://localhost:5173/confirmacion/" + "?success=true",
            cancel_url="http://localhost:5173/confirmacion/" + "?canceled=true",
        )
    except Exception:
        return Response(
            {"detail": "Something went wrong when creating stripe checkout session"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return Response(checkout_session.url)


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
        purchase_data = ast.literal_eval(metadata["purchase_data"])

        invoice_id = create_invoice(
            metadata=metadata, payment_intent=session["payment_intent"]
        )
        invoice = Factura.objects.get(id=invoice_id)
        invoice_items = invoice.productos.all()

        context = {
            "invoice": invoice,
            "items": invoice_items,
            "subtotal": sum([item.precio * item.cantidad for item in invoice_items]),
        }
        pdf = create_pdf(template="invoice.html", context=context)
        send_email(
            to=[
                {"email": settings.SENDER_EMAIL},
                {"email": session["customer_details"]["email"]},
            ],
            subject="Detalles del pedido",
            html_content="Gracias por su compra",
            attachment=pdf,
            attch_name="factura.pdf",
        )

        update_products_and_cart_items(purchase_data=purchase_data)

    return Response(status=status.HTTP_200_OK)
