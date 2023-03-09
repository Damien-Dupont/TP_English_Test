from django import forms
from .models import Player

from django.core import validators
from django.core.exceptions import ValidationError


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['email', 'lastname', 'firstname', 'password', 'town']
        widgets = {'password': forms.PasswordInput()}


class ConjugaisonForm(forms.Form):
    preterit = forms.CharField(max_length=50, label="preterit")
    participe_passe = forms.CharField(max_length=50, label="participe_passe")
    infinitif = forms.CharField(max_length=50, label="base_verbale")
    traduction = forms.CharField(max_length=50, label="traduction")
