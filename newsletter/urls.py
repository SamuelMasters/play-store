from django.urls import path
from . import views

urlpatterns = [
    path('', views.handle_newsletter_signup, name='newsletter'),
    path('confirm/', views.confirm_subscription, name='confirm'),
]
