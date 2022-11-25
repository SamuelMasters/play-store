from django import template


register = template.Library()


@register.filter(name='calculate_subtotal')
def calculate_subtotal(price, quantity):
    """ Used for calculating subtotal on bag.html """
    return price * quantity
