from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Product, Category


def display_products(request):
    """ A view to show users a list of products with optional filters """
    products = Product.objects.all()
    query = None
    platform = None

    if request.GET:
        if 'platform' in request.GET:
            platform = request.GET['platform']
            products = products.filter(platform=platform)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, 'No seach criteria was entered.\
                    Please check your query and try again.')
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'platform': platform,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show users the specific detail page for a given product """
    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
