# Generated by Django 4.2.4 on 2023-08-09 12:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0007_alter_profilepicture_status_likes'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Likes',
            new_name='PostLike',
        ),
    ]
