from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from . import models


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = models.CustomUser
    list_display = ('email','nome', 'telefone', 'is_staff', 'is_active',)
    list_filter = ('email','nome', 'telefone', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email','nome', 'telefone', 'password')}),
        ('Permição', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Register your models here.
admin.site.register(models.Programacao)
admin.site.register(models.Palestrante)
admin.site.register(models.Evento)
admin.site.register(models.CustomUser, CustomUserAdmin)