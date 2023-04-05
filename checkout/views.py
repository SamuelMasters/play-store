from django.shortcuts import render, redirect, reverse, get_object_or_404,\
    HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

from .forms import OrderForm
from .models import OrderLineItem, Order
from products.models import Product
from user_profiles.forms import UserProfileForm
from user_profiles.models import UserProfile
from bag.contexts import bag_contents
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

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
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save()
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
            return redirect(reverse('checkout_success',
                            args=[order.order_number]))
        else:
            messages.error(request, 'There was a problem with your order form.\
                Please check your information.')

    # occurs on GET request, such as load of checkout.html template
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "Your bag is empty.")
            return redirect(reverse('home'))

        current_bag = bag_contents(request)
        total = current_bag['total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'full_name': profile.default_full_name,
                    'email': request.user.email,
                    'street_address1': profile.default_street_address1,
                    'street_address2': profile.default_street_address2,
                    'postcode': profile.default_postcode,
                    'county': profile.default_county,
                    'country': profile.default_country,
                })
            except Exception as e:
                print(f"ERROR: the following exception occured: {e}")
                order_form = OrderForm()

    if not request.user.is_authenticated:
        order_form = OrderForm()

    if not stripe_secret_key:
        message.warning(request, 'Stripe public key was not found. Please \
                                check environment.')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

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
                'default_full_name': order.full_name,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_postcode': order.postcode,
                'default_county': order.county,
                'default_country': order.country,
            }
            user_profile_form = UserProfileForm(profile_data, instance=profile)

            if user_profile_form.is_valid():
                user_profile_form.save()

    message = Mail(
        from_email=settings.FROM_EMAIL,
        to_emails=order.email,
        subject=f'Your Play-Store order {order_number} has been confirmed!',
        html_content=f'Thank you for placing an order with us!\
                      Your order ID is <strong>"{order_number}"</strong>.<br>\
                      Please do not hesistate to contact us if you have \
                      any queries.',
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
    except Exception as e:
        print(f"ERROR: the following exception occurred when attempting \
            to send order confirmation: {e}")
        messages.error(request, 'There was a problem sending\
            the confirmation email. Please contact us for assistance.')

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
