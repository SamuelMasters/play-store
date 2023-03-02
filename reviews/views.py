from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages

from .models import ProductReview


def delete_review(request, review_id):
    """ Handles the deletion of reviews from the database """
    review = get_object_or_404(ProductReview, pk=review_id)
    if review.reviewer == request.user:
        review.delete()
        messages.success(request, 'Your review has been deleted.')
        return redirect(reverse('home'))
    else:
        messages.error(request, "You cannot delete the reviews of other\
                                 users.")
        return redirect(reverse('home'))
