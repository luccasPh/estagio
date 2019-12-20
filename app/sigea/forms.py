from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

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
        fields = ["titulo", "data_inicio", "data_fim", "local", "banner", "sobre", "capa"]
    
    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        self.fields['capa'] = forms.ImageField(required=False, error_messages = {'invalid':_("Selecione apenas imagem.")}, widget=forms.FileInput)
        self.fields['banner'] = forms.ImageField(required=False, error_messages = {'invalid':_("Selecione apenas imagem.")}, widget=forms.FileInput)
    
class PalestranteForm(forms.ModelForm):

    class Meta:
        model = models.Palestrante
        fields = ["nome", "afiliacao", "imagem"]
    
    def __init__(self, *args, **kwargs):
        super(PalestranteForm, self).__init__(*args, **kwargs)
        self.fields['imagem'] = forms.ImageField(required=False, error_messages = {'invalid':_("Selecione apenas imagem.")}, widget=forms.FileInput)
    

class AtividadesFilterForm(forms.Form):
    atividade = forms.ChoiceField(required=False)
    
    def __init__(self, evento, *args, **kwargs):
        super(AtividadesFilterForm, self).__init__(*args, **kwargs)
        self.fields['atividade'] = forms.ModelChoiceField(queryset=models.Programacao.objects.filter(evento=evento).filter(inscrever=True), required=False)
        self.fields['atividade'].empty_label = "Tudo"

class ProgramacaoForm(forms.ModelForm):
    
    class Meta:
        model = models.Programacao
        fields = ["titulo", "data_hora", "tipo", "palestrante", "inscrever"]
    
    def __init__(self, evento, *args, **kwargs):
        super(ProgramacaoForm, self).__init__(*args, **kwargs)
        self.fields['palestrante'].empty_label = "Sem palestrante"
        self.fields['palestrante'].queryset = models.Palestrante.objects.filter(
                                            evento=evento)

class InscricaoForm(forms.ModelForm):
    
    class Meta:
        model = models.Inscricao
        fields = ["cpf", "nome", "email", "telefone", "endereco", "faculdade", "curso", "atividade"]
    
    def __init__(self, evento, *args, **kwargs):
        super(InscricaoForm, self).__init__(*args, **kwargs)
        self.fields['atividade'].widget = forms.CheckboxSelectMultiple()
        self.fields['atividade'].queryset = models.Programacao.objects.filter(
                                            evento=evento).filter(inscrever=True).order_by('data_hora')