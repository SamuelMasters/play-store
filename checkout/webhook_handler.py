from django.http import HttpResponse


class StripeWH_Handler:
    """ Process Stripe Webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ Process non-specific or unexpected webhook events """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_succeeded(self, event):
        """ Process successful payment_intent webhook events """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )

    def handle_payment_intent_failed(self, event):
        """ Process failed payment_intent webhook events """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
