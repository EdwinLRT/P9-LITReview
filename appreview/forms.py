from django import forms

from . import models

class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'caption']

class ProductForm(forms.ModelForm):
    class Meta:
        model = models.Appreview
        fields = ['title', 'content', 'starred']