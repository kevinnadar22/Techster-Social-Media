# Generated by Django 4.0.5 on 2022-06-18 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0007_remove_usereditprofile_favourites_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usereditprofile',
            name='favorites',
        ),
    ]
