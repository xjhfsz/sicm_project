from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.utils import timezone
from datetime import date
from .forms import MoradorRegisterForm, AutorizacaoForm
from .models import Autorizacao, Morador


def home(request):
    """View for the home page."""
    return render(request, 'home.html')


def register(request):
    """
    View for the registration form.
    View para cadastro

    Se o formulário for válido, o usuário é logado e redirecionado para a dashboard.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
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
    """
    View para dashboard do morador

    Se usuário for morador, a dashboard é exibida.
    Se usuário não for morador, mensagem de erro é exibida e o usuário é redirecionado para a home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
    try:
        morador = request.user.morador
    except Morador.DoesNotExist:
        messages.error(request, 'Perfil de morador não encontrado. Contate o síndico.')
        return redirect('home')
    
    autorizacoes = morador.autorizacoes.all().order_by('-criado_em')
    return render(request, 'morador_dashboard.html', {'autorizacoes': autorizacoes})

@login_required
def cadastrar_visitante(request):
    """
    View para cadastro de autorização

    Se usuário for morador, o formulário de autorização é exibido.
    Se usuário não for morador, mensagem de erro é exibida e o usuário é redirecionado para a home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.
    """
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
    """
    View para lista de autorizaçãoes ativas
    """
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
    """View para login do usuario"""
    template_name = 'login.html'

class CustomLogoutView(LogoutView):
    """View para logout do usuario"""
    next_page = 'home'
    