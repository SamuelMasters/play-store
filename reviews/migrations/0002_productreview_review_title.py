# Generated by Django 3.2 on 2023-03-01 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productreview',
            name='review_title',
            field=models.CharField(blank=True, max_length=75, null=True),
        ),
    ]