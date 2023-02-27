from django.contrib import admin
from .models import Subscriber


class SubscriberAdmin(admin.ModelAdmin):
    model = Subscriber

    readonly_fields = ('confirmation_key', 'signup_date')

    fields = ('email', 'consent', 'signup_date', 'confirmation_key')

    list_display = (
        'email',
        'consent',
        'signup_date',
    )

    ordering = ('-signup_date',)


admin.site.register(Subscriber, SubscriberAdmin)
