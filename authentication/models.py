from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    MODERATOR = 'MODERATOR'
    REVIEWER = 'REVIEWER'
    AUTHOR = 'AUTHOR'

    ROLES_CHOICES = (
        (MODERATOR, 'Moderator'),
        (REVIEWER, 'Reviewer'),
        (AUTHOR, 'Author'),
    )
    profile_picture = models.ImageField()
    role = models.CharField(max_length=30, choices=ROLES_CHOICES, verbose_name='rôle', default=REVIEWER)
    pass
# Create your models here.
