# Generated by Django 3.2 on 2023-03-26 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profiles', '0002_auto_20230219_1326'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='default_full_name',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
    ]
