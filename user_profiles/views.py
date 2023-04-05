from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from .models import UserProfile
from .forms import UserProfileForm
from checkout.models import Order


def user_profile(request):
    """
    A view for displaying a user's saved address information and order history
    """
    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)

        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Changes to your profile have \
                                            been saved.')

        form = UserProfileForm(instance=profile)
        orders = profile.orders.all()

        template = 'profiles/profile.html'
        context = {
            'form': form,
            'orders': orders,
        }

        return render(request, template, context)
    else:
        messages.error(request, "You must be logged in to view your profile.")
        return redirect(reverse('home'))


def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}.'
        ' A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
