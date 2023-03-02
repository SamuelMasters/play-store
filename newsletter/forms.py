from django import forms
from .models import Subscriber


class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        """ Setup new subscriber form and assign placeholders """
        super().__init__(*args, **kwargs)
        placeholder = 'Enter your email address here.'

        self.fields['email'].widget.attrs['autofocus'] = True
        self.fields['email'].widget.attrs['placeholder'] = placeholder
        self.fields['email'].label = False
