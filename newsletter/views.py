from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

import random
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import Subscriber
from .forms import SubscriberForm


# Helper
def generate_confirmation_key():
    """
    Returns a 10-digit random number. 
    """
    return "%0.10d" % random.randint(0, 9999999999)


def handle_newsletter_signup(request):
    """

    """
    if request.method == 'POST':
        new_confirmation_key = generate_confirmation_key()
        form_data = {
            'email': request.POST['email'],
            'confirmation_key': new_confirmation_key,
        }
        new_subscriber = SubscriberForm(form_data)
        if new_subscriber.is_valid():
            new_subscriber.save()
            message = Mail(
                from_email=settings.FROM_EMAIL,
                to_emails=form_data['email'],
                subject='Play Store Newsletter Confirmation',
                html_content='Thanks for signing up to the Play.com \
                                newsletter! Please finish your signup by \
                                clicking <a href="{}/confirm/?email={}&confirmation_key={}">here</a> to confirm your registration.'.format(request.build_absolute_uri('/confirm/'),
                                form_data['email'],
                                form_data['confirmation_key']))

            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
                messages.success(request, 'Thanks for signing up! You will need \
                                        to check your email to finish your \
                                        signup.')
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                messages.error(request, 'There was a problem signing up.\
                                         Please try again later.')
                print(e)

            template = 'newsletter/newsletter.html'
            context = {
                'email': form_data['email'],
                'action': 'added',
                'form': SubscriberForm,
            }
            return render(request, template, context)
    else:
        template = 'newsletter/newsletter.html'
        context = {
            'form': SubscriberForm,
        }
        return render(request, template, context)
