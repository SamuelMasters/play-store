from django.db import models

from products.models import Product
from user_profiles.models import UserProfile


class ProductReview(models.Model):
    """ A model for representing product reviews """
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    reviewer = models.ForeignKey(UserProfile, related_name='reviewer', on_delete=models.CASCADE)
    review_title = models.CharField(max_length=75 ,null=True, blank=True)
    review_body = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
