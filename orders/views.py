import stripe
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from stripe.error import SignatureVerificationError

from django_stripe_integration import settings, helper
from orders.models import Order
from product.models import Product


@method_decorator(csrf_exempt, name='dispatch')
class OrderCompleteHook(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session_id = event['data']['object']['id']
            order = Order.objects.filter(checkout_session=session_id).first()
            if order:
                order.paid = True
                order.save()
                print("Payment was successful.")

        return HttpResponse(status=200)


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
            Order.objects.create(product=product,
                                 checkout_session=checkout_session['id'])
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)})
