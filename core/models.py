from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date


class Morador(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='morador')
    unidade = models.CharField('Unidade', max_length=10)
    telefone = models.CharField('Telefone', max_length=15, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.unidade}"

class Autorizacao(models.Model):
    morador = models.ForeignKey(Morador, on_delete=models.CASCADE, related_name='autorizacoes')
    nome_visitante = models.CharField('Nome do visitante', max_length=100)
    data_inicio = models.DateField('Data inicial')
    criado_em = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.data_inicio < date.today():
            raise ValidationError('Não é permitido criar autorização para data passada.')

    def is_active(self):
        hoje = date.today()
        return self.data_inicio == hoje

    def __str__(self):
        return f"{self.nome_visitante} - {self.morador.unidade} ({self.data_inicio})"
    