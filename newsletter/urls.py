from django.urls import path
from . import views

urlpatterns = [
    path('', views.handle_newsletter_signup, name='newsletter'),
]