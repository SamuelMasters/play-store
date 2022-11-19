from django.contrib import admin
from .models import Product, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'platform',
        'rating',
        'price',
    )

    ordering = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
