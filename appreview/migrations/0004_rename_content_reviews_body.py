# Generated by Django 4.2.2 on 2023-06-26 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appreview', '0003_alter_photo_image_reviews'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reviews',
            old_name='content',
            new_name='body',
        ),
    ]