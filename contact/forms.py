from django import forms
from .models import ContactQuery


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactQuery
        fields = ('first_name', 'last_name', 'email', 'query_body')

    def __init__(self, *args, **kwargs):
        """ Setup contact query form and assign placeholders """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Surname',
            'email': 'Email Address',
            'query_body': 'Please enter your query here.',
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields[field].widget.attrs['placeholder'] = placeholder
