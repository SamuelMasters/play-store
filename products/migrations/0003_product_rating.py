# Generated by Django 3.2 on 2023-03-01 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], default=3, max_length=1),
            preserve_default=False,
        ),
    ]
