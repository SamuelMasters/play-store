from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
import time

from .models import Product, Category
from .forms import ProductForm

# Below view has been adapted from Boutique Ado's equivalent, in particular the
# 'q' logic which enables the search bar to make queries


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


def add_product(request):
    """ Handles the creation of new products to the database """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product, please check the product details and try again.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your changes have been saved.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product - please check the update form for errors.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You're editing {product.name}.")

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)
