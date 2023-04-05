from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.db.models import Q

import time

from .models import Product, Category
from .forms import ProductForm
from reviews.forms import ReviewForm
from reviews.models import ProductReview

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

            queries = Q(name__icontains=query) \
                | Q(description__icontains=query)
            products = products.filter(queries)

    context = {
        'products': products,
        'search_term': query,
        'platform': platform,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """
    A view to show users the specific detail page for a given product and
    handle the submission of reviews on the page
    """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST' and request.user.is_authenticated:
        # Handles the submission product reviews based on form data
        form_data = {
            'product': product_id,
            'review_title': request.POST['review_title'],
            'review_body': request.POST['review_body'],
            'rating': request.POST['rating'],
            'reviewer': request.user,
        }

        rating = request.POST.get('rating', 3)
        review_title = request.POST.get('review_title')
        review_body = request.POST.get('review_body')
        review = ProductReview.objects.create(product=product,
                                              reviewer=request.user,
                                              rating=rating,
                                              review_title=review_title,
                                              review_body=review_body)

        try:
            review.save()
            messages.success(request, 'Thanks for leaving your feedback!\
                                        Your review has been saved.')
            form = ReviewForm()
            context = {
                'product': product,
                'form': form,
            }
            return render(request, 'products/product_detail.html', context)
        except Exception as e:
            messages.error(request, 'It looks like there was a problem\
                                     with your review. Please try again\
                                     later.')
            print(f"ERROR: An exception occurred: {e}")

    form = ReviewForm()
    context = {
        'product': product,
        'form': form,
    }
    return render(request, 'products/product_detail.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.is_superuser, login_url='/404/')
def add_product(request):
    """ Handles the creation of new products to the database """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product, please check the \
                                        product details and try again.')
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.is_superuser, login_url='/404/')
def edit_product(request, product_id):
    """ Handles the changing of existing product data """
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your changes have been saved.')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product - please check\
                           the update form for errors.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f"You're editing {product.name}.")

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required(login_url='/accounts/login/')
@user_passes_test(lambda u: u.is_superuser, login_url='/404/')
def delete_product(request, product_id):
    """ Handles the deletion of products from the database """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product successfully deleted.')
    return redirect(reverse('products'))
