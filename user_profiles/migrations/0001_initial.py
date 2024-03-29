# Generated by Django 3.2 on 2023-02-17 16:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('default_phone_number', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None)),
                ('default_full_name', models.CharField(blank=True, max_length=60, null=True)),
                ('default_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('default_street_address1', models.CharField(blank=True, max_length=90, null=True)),
                ('default_street_address2', models.CharField(blank=True, max_length=90, null=True)),
                ('default_postcode', models.CharField(blank=True, max_length=25, null=True)),
                ('default_county', models.CharField(blank=True, max_length=90, null=True)),
                ('default_country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
