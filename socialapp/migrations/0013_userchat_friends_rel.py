# Generated by Django 4.2.4 on 2023-08-11 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0012_userchat'),
    ]

    operations = [
        migrations.AddField(
            model_name='userchat',
            name='friends_rel',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='socialapp.friendrequest'),
        ),
    ]
