from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import OrderLineItem, Order
from products.models import Product
from user_profiles.forms import UserProfileForm
from user_profiles.models import UserProfile
from bag.contexts import bag_contents

import stripe
import json


# Below views adapated for use here from Boutique Ado project
def checkout(request):
    """
    A view for submitting payments to Stripe, and creating
    new instances of Order when the order is successfully placed.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        print("DEBUG: checkout view called as POST request")
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            # 'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            print("DEBUG: order_form recognised as valid...")  # debug
            order = order_form.save()
            print(f"DEBUG: order initialised: {order}")  # debug
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our \
                            database. "
                        "Please contact us for assistance.")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was a problem with your order form.\
                Please check your information.')
            # CRITICAL BUG: if form validation fails, then intent does not get created
            # for local scope, leading to crash - issue with phone number failing
            # need to account for failure of form variables
            print(order_form.errors.as_data()) # debug line, remove before deploy

    # occurs on GET request, such as load of checkout.html template
    else:
        print("DEBUG: checkout view called as GET request")  # debug line, remove before deploy
        bag = request.session.get('bag', {})
        print(f"DEBUG: bag retrieved: {bag}")  # debug
        if not bag:
            messages.error(request, "Your bag is empty.")
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        print(f"DEBUG: current_bag: {current_bag}")  # debug
        total = current_bag['total']
        print(f"DEBUG: total: {total}")  # debug
        stripe_total = round(total * 100)
        print(f"DEBUG: stripe_total: {stripe_total}")  # debug
        stripe.api_key = stripe_secret_key
        print(f"DEBUG: stripe.api_key: {stripe.api_key}")  # debug
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )
        print(f"DEBUG: intent: {intent}")  # debug
        order_form = OrderForm()

    if not stripe_secret_key:
        message.warning(request, 'Stripe public key was not found. Please \
                                check environment.')

    template = 'checkout/checkout.html'
    print("Assembling context...")  # debug
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
        # can the client_secret be passed here from a hidden input?
        # 'client_secret': client_secret,
    }
    print("Context assembled...")  # debug

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    A view for rendering an order confirmation page to the user.
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                # 'default_phone_number': order.phone_number,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_postcode': order.postcode,
                'default_county': order.county,
                'default_country': order.country,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)

            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully placed! \
        Your order number is {order_number}, and a confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


@require_POST
def cache_checkout_data(request):
    """ Adds checkout metadata to payment intent """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'username': request.user,
            'save_info': request.POST.get('save_info'),
            'bag': json.dumps(request.session.get('bag', {})),
        })
        return HttpResponse(status=200)
    except Exception as exception:
        messages.error(request, 'Unfortunately your pamyent cannot be \
            processed at the moment. Please try again later.')
        return HttpResponse(content=exception, status=400)
