import stripe
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics

from django_stripe_integration import settings, helper
from product.models import Product


@method_decorator(csrf_exempt, name='dispatch')
class Checkout(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        product_id = kwargs['product']
        product = Product.objects.get(id=product_id)
        price = int(product.price * 100)
        domain_url = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'products/',
                cancel_url=domain_url + 'products/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': product.name,
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': int(helper.add_service_fee(price)),
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})
