# Generated by Django 4.2.4 on 2023-08-11 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0009_friendrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]