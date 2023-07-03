from django import forms


from . import models
from .models import UserFollows
from authentication.models import User


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image']

class TicketForm(forms.ModelForm):
    class Meta:
        model = models.Ticket
        fields = ['title', 'content']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = models.Review
        fields = ['name','body']


class UserSearchForm(forms.Form):
    search_query = forms.CharField(label='Recherche d\'utilisateurs')