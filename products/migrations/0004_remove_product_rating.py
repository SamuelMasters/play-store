# Generated by Django 3.2 on 2023-03-01 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rating',
        ),
    ]