import stripe
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from stripe.error import SignatureVerificationError

from django_stripe_integration import settings, helper
from orders.models import Order
from product.models import Product

