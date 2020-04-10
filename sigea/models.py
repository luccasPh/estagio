from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from .manager import CustomUserManager
from autoslug import AutoSlugField
from tinymce.models import HTMLField
from cloudinary.models import CloudinaryField
from django.db.models.signals import pre_save
from django.dispatch import receiver

import os
import cloudinary.uploader
import cloudinary.api

# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=75)
    telefone = models.CharField(max_length=16)
    is_staff = models.BooleanField(_('gerência'), default=False,
        help_text=_('Designa se o usuário pode efetuar login neste administrador.'))
    is_active = models.BooleanField(_('ativo'), default=True,
        help_text=_('Designa se esse usuário deve ser tratado como ativo. Desmarque isso em vez de excluir contas.'))

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = _('organização')
        verbose_name_plural = _('organizações')

class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    data_inicio = models.DateField()
    data_fim = models.DateField()
    local = models.CharField(max_length=125, blank=True)
    banner = CloudinaryField('imagem', folder="media/eventos/banners/")
    organizacao = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    slug = AutoSlugField(max_length=200, populate_from='titulo', always_update=True)
    sobre = models.TextField(blank=True)
    capa = CloudinaryField('imagem', folder="media/eventos/capas/")

    def save(self, *args, **kwargs):
        if self.id != None:
            if not isinstance(self.banner, cloudinary.CloudinaryResource):
                old_banner = Evento.objects.get(id=self.id)
                cloudinary.uploader.destroy(old_banner.banner.public_id)

            if not isinstance(self.capa, cloudinary.CloudinaryResource):
                old_capa = Evento.objects.get(id=self.id)
                cloudinary.uploader.destroy(old_capa.capa.public_id)
        
        else:
            self.banner = cloudinary.uploader.upload_resource('sigea/static/img/none-banner.png', folder="media/eventos/banners/")
            self.capa = cloudinary.uploader.upload_resource('sigea/static/img/none-capa.png', folder="media/eventos/capas/")

        super(Evento, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        all_imagems = [self.banner.public_id, self.capa.public_id] 
        pale = Palestrante.objects.filter(evento_id=self.id)
        for img in pale:
            all_imagems.append(img.imagem.public_id)

        cloudinary.api.delete_resources(all_imagems)
        super(Evento, self).delete(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Programacao(models.Model):
    titulo = models.CharField(max_length=200)
    data_hora = models.DateTimeField()
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=45)
    palestrante = models.ForeignKey('Palestrante', blank=True, null=True, on_delete=models.SET_NULL)
    
    BOOL_CHOICES = ((True, 'Sim'), (False, 'Não'))
    inscrever = models.BooleanField(default=False, choices=BOOL_CHOICES)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name_plural = "Programações"


class Palestrante(models.Model):
    nome = models.CharField(max_length=45)
    afiliacao = models.CharField(max_length=45, blank=True)
    imagem = CloudinaryField('imagem', folder="media/palestrantes/")
    evento = models.ForeignKey('Evento', on_delete=models.CASCADE)

    
    def save(self, *args, **kwargs):
        if self.id != None:
            if not isinstance(self.imagem, cloudinary.CloudinaryResource):
                old_imagem = Palestrante.objects.get(id=self.id)
                cloudinary.uploader.destroy(old_imagem.imagem.public_id)
        
        else:
            if self.imagem == None:
                self.imagem = cloudinary.uploader.upload_resource('sigea/static/img/none-foto.png', folder="media/palestrantes/")

        super(Palestrante, self).save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        cloudinary.uploader.destroy(self.imagem.public_id)
        super(Palestrante, self).delete(*args, **kwargs)

    

    def __str__(self):
        return self.nome

class Inscricao(models.Model):
    cpf = models.CharField(max_length=14)
    nome = models.CharField(max_length=45)
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=16)
    endereco = models.CharField(max_length=125)
    faculdade = models.CharField(max_length=50, blank=True)
    curso = models.CharField(max_length=50, blank=True)
    atividade = models.ManyToManyField("Programacao", blank=True)
    evento = models.ForeignKey("Evento", on_delete=models.CASCADE)
    data_inscricao = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Inscricões"
    
    def __str__(self):
        return self.nome
    
    def id_cpf(self):
        res = self.cpf.replace(".","").replace("-","")
        return res
