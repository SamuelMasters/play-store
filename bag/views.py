from django.shortcuts import render, redirect, reverse, HttpResponse


def view_bag(request):
    """ A view to render the bag template """

    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """ A view to handle adding items to the bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)


def edit_bag(request, item_id):
    """ A view to handle editing item quantities already in the bag """

    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
    else:
        bag.pop(item_id)

    request.session['bag'] = bag
    print("edit_bag view was called")
    return redirect(reverse('view_bag'))


def delete_from_bag(request, item_id):
    """ A view to handle removing items from the bag """

    try:
        bag = request.session.get('bag', {})
        bag.pop(item_id)

        request.session['bag'] = bag
        print("delete_from_bag view was called and returned status 200")
        return HttpResponse(status=200)
    except Exception as error:
        print("delete_from_bag view returned error 500")
        return HttpResponse(status=500)
