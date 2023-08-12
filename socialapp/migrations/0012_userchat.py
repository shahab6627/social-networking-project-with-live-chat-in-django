# Generated by Django 4.2.4 on 2023-08-11 14:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialapp', '0011_alter_friendrequest_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('msg_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_from', to=settings.AUTH_USER_MODEL)),
                ('msg_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
