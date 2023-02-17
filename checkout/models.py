import uuid

from django.db import models
from django.db.models import Sum
from django.conf import settings
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from products.models import Product
from user_profiles.models import UserProfile


class Order(models.Model):
    """ A model to represent an instance of a customer order """
    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    date = models.DateTimeField(auto_now_add=True)
    full_name = models.CharField(max_length=60, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    """
    Custom phone_number field from \
        https://django-phonenumber-field.readthedocs.io/en/latest/
    """
    phone_number = PhoneNumberField(blank=True)
    street_address1 = models.CharField(max_length=90, null=False, blank=False)
    street_address2 = models.CharField(max_length=90, null=True, blank=True)
    """ Custom country field from \
        https://pypi.org/project/django-countries/
    """
    county = models.CharField(max_length=90, null=True, blank=True)
    postcode = models.CharField(max_length=25, null=False, blank=False)

    country = CountryField()
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def _assign_order_number(self):
        """ Generates the order number to associate with each order instance """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Triggers order number creation if one does not already exist
        at the time the order is saved
        """
        if not self.order_number:
            self.order_number = self._assign_order_number()
        super().save(*args, **kwargs)

    def update_total(self):
        """
        Updates the order_total when a new line item is added
        """
        self.order_total = self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum']
        self.save()

    def __str__(self):
        return self.order_number


class OrderLineItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False, blank=False, related_name='lineitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False, blank=False)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Triggers order number creation if one does not already exist
        at the time the order is saved
        """
        self.lineitem_total = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Item "{self.product.name}" on order {self.order.order_number}'
