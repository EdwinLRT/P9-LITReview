# Generated by Django 4.2.2 on 2023-06-26 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appreview', '0005_rename_reviews_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='title',
            new_name='name',
        ),
    ]
