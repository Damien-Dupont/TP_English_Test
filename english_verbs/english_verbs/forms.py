from django import forms
from .models import Player


class SignUpForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['email', 'lastname', 'firstname', 'password', 'town']
        widgets = {'password': forms.PasswordInput()}

# class InscriptionForm(forms.Form):
#    nom = forms.CharField(label="Nom", max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Votre nom', 'class':'inputChamp'}))
#    pseudo = forms.CharField(label="Pseudo", max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Votre pseudo', 'class':'inputChamp'}))
#    email = forms.EmailField(label="Email", max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Votre email', 'class':'inputChamp'}))
#    mdp = forms.CharField(label="Mot de passe", max_length=200, widget=forms.PasswordInput(attrs={'class':'inputChamp'}))


class ConjugaisonForm(forms.Form):
    preterit = forms.CharField(max_length=50, label="preterit")
    participe_passe = forms.CharField(max_length=50, label="participe_passe")
    base_verbale = forms.CharField(max_length=50, label="base_verbale")
    traduction = forms.CharField(max_length=50, label="traduction")
