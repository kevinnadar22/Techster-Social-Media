# Generated by Django 4.0.5 on 2022-06-26 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_post_comments_post_is_comment_disabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='posted_comments',
            field=models.ManyToManyField(blank=True, related_name='post_comments', to='core.comments'),
        ),
    ]
