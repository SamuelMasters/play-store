from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "Your bag is empty.")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51M8Pr9JTdnqrnmtwQBk5B1UBH7GdE8A9bR5u1c1uw0Qs0wbIMUgC7x9ywl6uVwBfMHrEBVhSAZd1h15omnLraW1s00NOD2nNHF',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)
