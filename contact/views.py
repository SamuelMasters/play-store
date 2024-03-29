from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .models import ContactQuery
from .forms import ContactForm


def contact(request):
    """
    A view for rendering the contact form to users, and submitting
    user queries created from that form.
    """
    if request.method == 'POST':
        form_data = {
            'subject': request.POST['subject'],
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'query_body': request.POST['query_body'],
        }
        query_form = ContactForm(form_data)
        if query_form.is_valid():
            query_form.save()
            messages.success(request, 'Your message has been sent! We will try\
                                       to get back to you within 24 hours.')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'There was a problem with your query.\
                Please check the query form and try again.')

    query_form = ContactForm()
    template = 'contact/contact.html'
    context = {
        'query_form': query_form,
    }

    return render(request, template, context)
