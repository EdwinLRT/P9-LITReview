# Generated by Django 4.2.2 on 2023-07-03 09:28

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_user_followers_alter_user_following'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='following',
        ),
        migrations.AddField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='suit'),
        ),
    ]
