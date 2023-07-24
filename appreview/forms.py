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
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # Les choix vont de 1 à 5
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select)
    class Meta:
        model = models.Review
        fields = ['rating', 'name', 'body']

class UserSearchForm(forms.Form):
    search_query = forms.CharField(label='Recherche d\'utilisateurs')