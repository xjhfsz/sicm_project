from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date


class Morador(models.Model):
    """Modelo do Morador"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='morador')
    unidade = models.CharField("Unidade / Apartamento", max_length=50)
    telefone = models.CharField("Telefone", max_length=20)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - Unidade: {self.unidade}"

class Autorizacao(models.Model):
    """Modelo de Autorização"""
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE, related_name='autorizacoes')
    nome_visitante = models.CharField('Nome do visitante', max_length=100)
    data_inicio = models.DateField('Data da Visita')
    criado_em = models.DateTimeField(auto_now_add=True)

    def clean(self):

        # Validação: impede autorizações para datas anteriores ao dia atual
        if self.data_inicio and self.data_inicio < date.today():
            raise ValidationError('Não é permitido criar autorização para data inferior a hoje.')

    def is_active(self):
        return self.data_inicio == date.today()

    def __str__(self):
        return f"{self.nome_visitante} - {self.morador.unidade} ({self.data_inicio})"
    