from django.contrib import admin
from .models import ProductReview


class ReviewAdmin(admin.ModelAdmin):
    model = ProductReview
    list_display = (
        'review_title',
        'rating',
        'product',
        'reviewer',
    )


admin.site.register(ProductReview, ReviewAdmin)
