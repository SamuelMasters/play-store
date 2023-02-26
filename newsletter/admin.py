from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    model = Subscriber
    list_display = (
        'email',
        'consent',
        'signup_date',
    )

    ordering = ('-signup_date',)


admin.site.register(Subscriber, SubscriberAdmin)
