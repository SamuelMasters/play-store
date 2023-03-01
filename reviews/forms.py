from django import forms
from .models import ProductReview


class ReviewForm(forms.ModelForm):
    #
    rating = forms.CharField(label='Rating', widget=forms.TextInput(attrs={'min':1,'max': '5','type': 'number'}))

    class Meta:
        model = ProductReview
        fields = ('review_title', 'review_body', 'rating')

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        placeholders = {
            'review_title': 'Title',
            'review_body': 'Write your review here.',
            'rating': 'Give the product a rating.',
        }

        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].label = False
