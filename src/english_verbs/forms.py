from django import forms
from .models import Player

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['email', 'lastname', 'firstname', 'password', 'town']
        widgets = {'password': forms.PasswordInput()}

class ConjugaisonForm(forms.Form):
    preterit = forms.CharField(max_length=50, label="preterit")
    past_participle = forms.CharField(max_length=50, label="past_participle")