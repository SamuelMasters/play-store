# Generated by Django 3.2 on 2023-03-26 16:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0003_userprofile_default_full_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='default_phone_number',
        ),
    ]
