import json
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import date
from .forms import CadastroMoradorForm, AutorizacaoForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Autorizacao, Morador # Ajuste conforme o nome do seu Model


def home(request):
    return render(request, 'home.html')


def cadastrar_morador(request):
    if request.method == 'POST':
        form = CadastroMoradorForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = form.save()
            Morador.objects.create(
                user=user,
                unidade=cleaned_data['unidade'],
                telefone=cleaned_data['telefone'],
            )
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('dashboard')
    else:
        form = CadastroMoradorForm()
    return render(request, 'cadastro.html', {'form': form})


def logar_morador(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def deslogar_morador(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard_morador(request):
    morador = request.user.morador
    if request.method == 'POST':
        form = AutorizacaoForm(request.POST)
        if form.is_valid():
            autorizacao = form.save(commit=False)
            autorizacao.morador = morador
            try:
                autorizacao.full_clean()
                autorizacao.save()
                messages.success(request, 'Visitante autorizado com sucesso!')
                return redirect('dashboard')
            except Exception as e:
                messages.error(request, 'Data inválida: não é permitido cadastrar data passada.')
    else:
        form = AutorizacaoForm()

    autorizacoes = morador.autorizacoes.all().order_by('-data_inicio')
    hoje = date.today()
    return render(request, 'home.html', {
        'form': form,
        'autorizacoes': autorizacoes,
        'hoje': hoje
    })




@csrf_exempt
def listar_criar_visitantes(request):
    if request.method == 'GET':
        # Busca todas as autorizações ordenadas pelas mais recentes
        autorizacoes = Autorizacao.objects.select_related('morador__user').all().order_by('-criado_em')
        data = [
            {
                'id': a.id,
                'nome': a.nome_visitante,
                'data_visita': a.data_inicio.strftime('%d/%m/%Y') if a.data_inicio else '',
                'unidade': a.morador.unidade if a.morador else 'N/A',
            }
            for a in autorizacoes
        ]
        return JsonResponse(data, safe=False)

    elif request.method == 'POST':
        try:
            body = json.loads(request.body)
            nome_visitante = body.get('nome')

            # Identifica o morador logado ou pega o primeiro disponível no banco para testes
            morador = None
            if request.user.is_authenticated and hasattr(request.user, 'morador'):
                morador = request.user.morador
            else:
                morador = Morador.objects.first()

            if not morador:
                return JsonResponse({'erro': 'Nenhum morador cadastrado no sistema.'}, status=400)

            # Cria a autorização com a data de hoje
            nova_aut = Autorizacao.objects.create(
                morador=morador,
                nome_visitante=nome_visitante,
                data_inicio=date.today()
            )

            return JsonResponse({
                'id': nova_aut.id,
                'nome': nova_aut.nome_visitante,
                'data_visita': nova_aut.data_inicio.strftime('%d/%m/%Y'),
                'unidade': nova_aut.morador.unidade,
                'mensagem': 'Autorização registrada no banco!'
            }, status=201)

        except Exception as e:
            return JsonResponse({'erro': str(e)}, status=400)


@csrf_exempt
def revogar_visitante(request, visitante_id):
    if request.method == 'DELETE':
        try:
            autorizacao = Autorizacao.objects.get(id=visitante_id)
            autorizacao.delete()
            return JsonResponse({'mensagem': 'Autorização revogada com sucesso!'}, status=200)
        except Autorizacao.DoesNotExist:
            return JsonResponse({'erro': 'Autorização não encontrada.'}, status=404)



def portaria_lista(request):
    hoje = date.today()
    query = request.GET.get('q', '')
    
    # Filtra apenas visitantes autorizados para a data atual
    autorizacoes_hoje = Autorizacao.objects.filter(data_inicio=hoje)

    if query:
        autorizacoes_hoje = autorizacoes_hoje.filter(nome_visitante__icontains=query)

    return render(request, 'portaria.html', {
        'autorizacoes': autorizacoes_hoje,
        'hoje': hoje,
        'query': query
    })
    