from django.contrib import admin
from .models import ContactQuery


class QueryAdmin(admin.ModelAdmin):
    model = ContactQuery
    list_display = (
        'subject',
        'first_name',
        'last_name',
        'email',
        'date',
    )

    ordering = ('date',)


admin.site.register(ContactQuery, QueryAdmin)
