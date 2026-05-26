from django.contrib import admin
from .models import Morador, Autorizacao

@admin.register(Morador)
class MoradorAdmin(admin.ModelAdmin):
    list_display = ('user', 'unidade', 'telefone')
    search_fields = ('user__username', 'unidade')

@admin.register(Autorizacao)
class AutorizacaoAdmin(admin.ModelAdmin):
    list_display = ('nome_visitante', 'morador', 'data_inicio')
    list_filter = ('data_inicio',)
