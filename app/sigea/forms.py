from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from . import models 

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = models.CustomUser
        fields = ('email','nome', 'telefone',)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = models.CustomUser
        fields = ('email','nome', 'telefone',)

class EventoForm(forms.ModelForm):
    class Meta:
        model = models.Evento
        fields = ["titulo", "data", "local", "banner"]

class ProgramacaoForm(forms.ModelForm):
    class Meta:
        model = models.Programacao
        fields = ["titulo", "data_hora", "atividade"]

class PalestranteForm(forms.ModelForm):
    class Meta:
        model = models.Palestrante
        fields = ["nome", "afiliacao", "imagem"]