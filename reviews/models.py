from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

from products.models import Product


class ProductReview(models.Model):
    """ A model for representing product reviews """
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, null=False, blank=False)
    reviewer = models.ForeignKey(User, related_name='reviewer', on_delete=models.CASCADE)
    review_title = models.CharField(max_length=75, null=True, blank=True)
    review_body = models.TextField(null=True, blank=True)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
