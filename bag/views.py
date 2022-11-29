from django.shortcuts import render, redirect, reverse, HttpResponse, \
    get_object_or_404
from django.contrib import messages
from products.models import Product

# Views adapated and customised for use from Boutique Ado walkthough project


def view_bag(request):
    """ A view to render the bag template """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ A view to handle adding items to the bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
        messages.success(request, f'Item quantity for {product.name} has been\
             updated to {bag[item_id]}.')
    else:
        bag[item_id] = quantity
        messages.success(request, f'You added x{quantity} {product.name} to \
            your bag!')

    request.session['bag'] = bag
    return redirect(redirect_url)


def edit_bag(request, item_id):
    """ A view to handle editing item quantities already in the bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(request, f'Item quantity for {product.name} has been\
             updated to {bag[item_id]}.')
    else:
        bag.pop(item_id)
        messages.success(request, f'{product.name} was removed from your bag.')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ A view to handle removing items from the bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        bag = request.session.get('bag', {})
        bag.pop(item_id)
        messages.success(request, f'{product.name} was removed from your bag.')

        request.session['bag'] = bag
        print("remove_from_bag view was called and returned status 200")
        return HttpResponse(status=200)
    except Exception as error:
        print("remove_from_bag view returned error 500")
        messages.error(request, f'Error removing item from bag: {e}')
        return HttpResponse(status=500)
