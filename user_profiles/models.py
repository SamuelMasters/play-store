from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(models.Model):
    """ A model to represent a user's saved information """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_full_name = models.CharField(max_length=40, null=True,
                                         blank=True)
    default_street_address1 = models.CharField(max_length=90, null=True,
                                               blank=True)
    default_street_address2 = models.CharField(max_length=90, null=True,
                                               blank=True)
    default_postcode = models.CharField(max_length=25, null=True, blank=True)
    default_county = models.CharField(max_length=90, null=True, blank=True)
    default_country = CountryField(blank_label='Country', null=True,
                                   blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_update_profile(sender, instance, created, **kwargs):
    """ Handles the creation or updating of a user profile """
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()
