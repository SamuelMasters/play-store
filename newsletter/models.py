from django.db import models


class Subscriber(models.Model):
    """
    A model to represent users who have passed their email address
    along to the application in order to receive promotional newsletters.
    """
    email = models.EmailField(max_length=254, null=False, blank=False)
    confirmation_key = models.CharField(max_length=10)
    consent = models.BooleanField(default=False)
    signup_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email + " (" + ("not " if not self.consent else "") + "confirmed)"
