from django.db import models


class ContactQuery(models.Model):
    """ A model to represent a submitted user query from a contact form """
    subject = models.CharField(max_length=254, null=False, blank=False)
    first_name = models.CharField(max_length=40, null=False, blank=False)
    last_name = models.CharField(max_length=40, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    query_body = models.TextField(null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Contact Queries'
