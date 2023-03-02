from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email',
                  'street_address1', 'street_address2',
                  'postcode', 'country', 'county')

    def __init__(self, *args, **kwargs):
        """ Setup the order form and add assign placeholders, classes """
        super().__init__(*args, **kwargs)
        placeholders = {
                'full_name': 'Full Name',
                'email': 'Email Address',
                'country': 'Country',
                'postcode': 'Postal Code',
                'street_address1': 'Street Address 1',
                'street_address2': 'Street Address 2',
                'county': 'County',
            }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
