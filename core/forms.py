from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Morador, Autorizacao

class CadastroMoradorForm(UserCreationForm):
    unidade = forms.CharField(label='Unidade / Apartamento', max_length=50)
    telefone = forms.CharField(label='Telefone', max_length=20)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['senha'],
            first_name=self.cleaned_data['nome']
        )
        morador = Morador.objects.create(
            user=user,
            unidade=self.cleaned_data['unidade'],
            telefone=self.cleaned_data['telefone']
        )
        return user

class AutorizacaoForm(forms.ModelForm):
    class Meta:
        model = Autorizacao
        fields = ['nome_visitante', 'data_inicio']
        widgets = {
            'nome_visitante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo do visitante'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        