from django import forms
from .models import ContactQuery


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactQuery
        fields = ('subject', 'first_name', 'last_name',
                  'email', 'query_body')

    def __init__(self, *args, **kwargs):
        """ Setup contact query form and assign placeholders """
        super().__init__(*args, **kwargs)
        placeholders = {
            'subject': 'Subject',
            'first_name': 'First Name',
            'last_name': 'Surname',
            'email': 'Email Address',
            'query_body': 'Please enter your query here.',
        }

        self.fields['subject'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
