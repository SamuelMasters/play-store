from django.shortcuts import render

from .models import Product, Category


def display_products(request):
    """ """
    products = Product.objects.all()

    context = {
        'products': products,
    }

    return render(request, 'products/products.html', context)
