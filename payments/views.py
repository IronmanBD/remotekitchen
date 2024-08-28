import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import Orders
from payments.models import Payment

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY
# Create your views here.
class PaymentAPI(APIView):
    def post(self, request, *args, **kwargs):
        order_id = kwargs.get('order_id')
        try:
            order = get_object_or_404(Orders, id=order_id)
        except Orders.DoesNotExist:
            return Response({"MSG": "order Not Found"}, status=status.HTTP_404_NOT_FOUND)

        total_amount = order.calculate_total

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Order {order.id}',
                        },
                        'unit_amount': int(total_amount * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=settings.PAYMENT_SUCCESS_URL,

            )

            payment = Payment.objects.create(
                order=order,
                amount=total_amount,
                checkout_session_id=checkout_session.id,
                payment_status='pending'
            )
            order.order_status = 'processing'
            order.save()
            return JsonResponse({
                'id': checkout_session.id,
                'order': order_id,
                'total': total_amount
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})

class StripeWebhookAPI(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
            )
        except ValueError:
            return JsonResponse({'error': 'Invalid payload'}, status=400)
        except stripe.error.SignatureVerificationError:
            return JsonResponse({'error': 'Invalid signature'}, status=400)

        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            session_id = session['id']
            order_id = session['metadata']['order_id']
            try:
                payment = Payment.objects.get(checkout_session_id=session_id)
                payment.stripe_payment_intent_id = session.get('payment_intent')
                payment.payment_status = 'complete'

                order = Orders.objects.get(id=order_id)
                order.payment_status = 'complete'
                order.save()
            except Payment.DoesNotExist:
                return JsonResponse({'error': 'Payment is not found'}, status=404)
            except Orders.DoesNotExist:
                return JsonResponse({'error': 'Order is not found'}, status=404)

            return JsonResponse({'status': 'success'})
