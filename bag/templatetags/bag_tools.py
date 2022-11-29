# bag_tools.py was taken from Boutique Ado for use in this project,
# as the functionality was required without changes for calculating
# subtotals at this project's checkout stage
from django import template


register = template.Library()


@register.filter(name='calculate_subtotal')
def calculate_subtotal(price, quantity):
    """ Used for calculating subtotal on bag.html """
    return price * quantity
