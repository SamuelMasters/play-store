# signals.py taken from Boutique Ado as the existing file was ideal
# for the requirements of this project
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """ Updates the order total when lineitems are created or updated """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_on_delete(sender, instance, **kwargs):
    """ Updates the order total when lineitems are deleted """
    instance.order.update_total()
