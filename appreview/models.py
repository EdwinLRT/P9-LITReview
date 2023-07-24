from io import BytesIO

from PIL import Image
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


class Photo(models.Model):
    image = models.ImageField(upload_to='products_photos/')
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Redimensionner et compresser l'image avant l'enregistrement du modèle
        if self.image:
            image = Image.open(self.image)
            image.thumbnail((800, 800))  # Redimensionne l'image à une taille maximale de 800x800 pixels

            # Créer un flux de mémoire pour enregistrer l'image
            output = BytesIO()
            image.save(output, format='JPEG', quality=80)  # Compression avec une qualité de 80%
            output.seek(0)

            # Enregistrer l'image redimensionnée et compressée dans le modèle
            self.image = InMemoryUploadedFile(output, 'ImageField', f"{self.image.name.split('.')[0]}.jpg",
                                              'image/jpeg', output.getbuffer().nbytes, None)

        # Appeler la méthode save() de la superclasse pour enregistrer le modèle
        super().save(*args, **kwargs)


class Ticket(models.Model):
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    title = models.CharField(max_length=128)
    content = models.CharField(max_length=5000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    starred = models.BooleanField(default=False)


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=80)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)  # 1, 2, 3, 4, 5
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Review {} by {}'.format(self.body, self.name)


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name="followed_by")

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('user', 'followed_user',)
