# Generated by Django 4.0.5 on 2022-06-22 19:15

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0008_remove_usereditprofile_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usereditprofile',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
    ]
