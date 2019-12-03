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
from django.contrib.auth.decorators import login_required

from . import views

app_name = "sigea"

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    path('', views.Index.as_view(), name="index"),
    path('organizador', views.Organizacao.as_view(), name="organizador"),
    path('programacao/add/', views.ProgramacaoCreate.as_view(), name="programacao_add"),
    path('programacao/<int:pk>/update/', views.ProgramacaoUpdate.as_view(), name="programacao_update"),
    path('programacao/<int:pk>/delete/', views.ProgramacaoDelete.as_view(), name="programacao_delete"),

    path('palestrante/add/', views.PalestranteCreate.as_view(), name="palestrante_add"),
    path('palestrante/<int:pk>/update/', views.PalestranteUpdate.as_view(), name="palestrante_update"),
    path('palestrante/<int:pk>/delete/', views.PalestranteDelete.as_view(), name="palestrante_delete"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)