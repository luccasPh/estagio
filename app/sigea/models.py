from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .manager import CustomUserManager

import os

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=75)
    telefone = models.CharField(max_length=25)
    is_staff = models.BooleanField(_('gerência'), default=False,
        help_text=_('Designa se o usuário pode efetuar login neste administrador.'))
    is_active = models.BooleanField(_('ativo'), default=True,
        help_text=_('Designa se esse usuário deve ser tratado como ativo. Desmarque isso em vez de excluir contas.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome','telefone']

    objects = CustomUserManager()

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = _('organização')
        verbose_name_plural = _('organizações')


class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    data = models.DateField()
    local = models.CharField(max_length=75)
    banner = models.ImageField(upload_to="evento/banner", blank=True)
    organizacao_idorganizacao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    apresentacao_titulo = models.CharField(max_length=200, blank=True)
    apresentacao_descricao = models.TextField(blank=True)
    apresentacao_capa = models.ImageField(upload_to="evento/capa", blank=True)

    

class Programacao(models.Model):
    titulo = models.CharField(max_length=200)
    data_hora = models.DateTimeField()

    OPCOES = (
        ("1", "Outros"),
        ("2", "Palestra"), 
        ("3", "Oficina"), 
        ("4", "Mesa Redona"), 
        ("5", "Mini Curso")
    )
    atividade = models.CharField(max_length=45, choices=OPCOES, default="1")

    def __str__(self):
        return self.titulo


class Palestrante(models.Model):
    nome = models.CharField(max_length=45)
    afiliacao = models.CharField(max_length=45)
    imagem = models.ImageField(upload_to="palestrantes", default="none.png")

    def __str__(self):
        return self.nome
