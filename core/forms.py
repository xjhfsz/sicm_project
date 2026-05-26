from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Morador, Autorizacao

class MoradorRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    unidade = forms.CharField(max_length=10, required=True)
    telefone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Morador.objects.create(
                user=user,
                unidade=self.cleaned_data['unidade'],
                telefone=self.cleaned_data.get('telefone', '')
            )
        return user

class AutorizacaoForm(forms.ModelForm):
    class Meta:
        model = Autorizacao
        fields = ['nome_visitante', 'data_inicio']
        widgets = {
            'data_inicio': forms.DateInput(attrs={'type': 'date'}),
        }
        