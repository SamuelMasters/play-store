from django.db import models


PLATFORM_CHOICES = (
    ('xbox', 'Xbox'),
    ('playstation', 'Playstation'),
    ('pc', 'PC'),
    ('board_game', 'Board Game'),
)


class Category(models.Model):
    """ A model for different categories of products """
    category_name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.category_name

    def get_friendly_name(self):
        return self.friendly_name

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    """ A model for items to sell on the site """
    category = models.ForeignKey('Category', null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField()
    platform = models.CharField(max_length=254, choices=PLATFORM_CHOICES)
    image_main = models.ImageField(null=True, blank=True)
    image_2 = models.ImageField(null=True, blank=True)
    image_3 = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
