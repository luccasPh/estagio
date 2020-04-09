"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from . import views

app_name = "sigea"

urlpatterns = [
    path('logout', views.Logout.as_view(), name='logout'),
    path('', views.Index.as_view(), name="index"),
    path('editar', views.EditarOrgnizacao.as_view(), name='editar'),

    path('evento/<int:evpk>/config', views.EventoConfig.as_view(), name="evento_config"),
    path('evento/<int:evpk>/config#filter', views.InscricaoFilter.as_view(), name="inscricao_filter"),
    path('evento/<int:evpk>/inscricao', views.InscricaoPage.as_view(), name="inscricao"),
    path('evento/<int:evpk>/inscricao/pdf/<int:prpk>', views.InscricaoPdf.as_view(), name="inscricao_pdf"),
    
    path('evento/add/', views.EventoCreate.as_view(), name="evento_add"),
    path('evento/<int:evpk>/delete/', views.EventoDelete.as_view(), name="evento_delete"),
    path('evento/<int:evpk>/<slug:slug>', views.EventoPage.as_view(), name="evento_pagina"),

    path('evento/<int:evpk>/programacao/add/', views.ProgramacaoCreate.as_view(), name="programacao_add"),
    path('evento/<int:evpk>/programacao/<int:prpk>/update/', views.ProgramacaoUpdate.as_view(), name="programacao_update"),
    path('evento/<int:evpk>/programacao/<int:prpk>/delete/', views.ProgramacaoDelete.as_view(), name="programacao_delete"),

    path('evento/<int:evpk>/palestrante/add/', views.PalestranteCreate.as_view(), name="palestrante_add"),
    path('evento/<int:evpk>/palestrante/<int:papk>/update/', views.PalestranteUpdate.as_view(), name="palestrante_update"),
    path('evento/<int:evpk>/palestrante/<int:papk>/delete/', views.PalestranteDelete.as_view(), name="palestrante_delete"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)