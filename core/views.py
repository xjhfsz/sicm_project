from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.utils import timezone
from datetime import date
from .forms import MoradorRegisterForm, AutorizacaoForm
from .models import Autorizacao, Morador


def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'POST':
        form = MoradorRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('morador_dashboard')
    else:
        form = MoradorRegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def morador_dashboard(request):
    try:
        morador = request.user.morador
    except Morador.DoesNotExist:
        messages.error(request, 'Perfil de morador não encontrado. Contate o síndico.')
        return redirect('home')
    
    autorizacoes = morador.autorizacoes.all().order_by('-criado_em')
    return render(request, 'morador_dashboard.html', {'autorizacoes': autorizacoes})

@login_required
def cadastrar_visitante(request):
    try:
        morador = request.user.morador
    except Morador.DoesNotExist:
        messages.error(request, 'Perfil de morador não encontrado.')
        return redirect('home')
    
    if request.method == 'POST':
        form = AutorizacaoForm(request.POST)
        if form.is_valid():
            autorizacao = form.save(commit=False)
            autorizacao.morador = morador
            autorizacao.save()
            messages.success(request, f'Autorização para {autorizacao.nome_visitante} criada com sucesso!')
            return redirect('morador_dashboard')
    else:
        form = AutorizacaoForm()
    return render(request, 'cadastrar_visitante.html', {'form': form})

def portaria_lista(request):
    hoje = date.today()
    autorizacoes_ativas = Autorizacao.objects.filter(
        data_inicio=hoje,
    ).select_related('morador').order_by('morador__unidade')
    
    # Filtro por nome se houver busca
    search_query = request.GET.get('q')
    if search_query:
        autorizacoes_ativas = autorizacoes_ativas.filter(nome_visitante__icontains=search_query)
    
    return render(request, 'portaria_lista.html', {
        'autorizacoes': autorizacoes_ativas,
        'search_query': search_query,
        'hoje': hoje
    })


from django.contrib.auth.views import LoginView, LogoutView

class CustomLoginView(LoginView):
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    next_page = 'home'