from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """ Adds placeholders, classes """
        super().__init__(*args, **kwargs)
        placeholders = {
                'default_full_name': 'Full Name',
                'default_country': 'Country',
                'default_postcode': 'Postal Code',
                'default_street_address1': 'Street Address 1',
                'default_street_address2': 'Street Address 2',
                'default_county': 'County',
            }

        self.fields['default_full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'rounded-0 \
                profile-form-input'
            self.fields[field].label = False
