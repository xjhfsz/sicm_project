# 🏢 SICM - Sistema de Identificação e Cadastro de Morador

Sistema web desenvolvido em **Django** para automatizar a autorização de entrada em condomínios residenciais.  
Substitui o processo manual (interfone + caderno) por um fluxo digital: o morador autoriza o visitante com antecedência e a portaria consulta a lista do dia.

## ✅ MVP - Funcionalidades Entregues

- Cadastro de moradores (nome, e-mail, unidade, telefone)
- Login de moradores (autenticação segura)
- Autorização de visitantes (nome + data da visita)
- Dashboard do morador (lista todas as suas autorizações, com status ativo/expirado)
- Tela da portaria (mostra **apenas os visitantes autorizados para o dia atual**, com busca por nome)
- Interface responsiva com Bootstrap 5

## 🛠️ Tecnologias

- Python
- Django 6.0.5
- SQLite3 (banco padrão – pode migrar para PostgreSQL depois)
- Bootstrap 5 (front-end)
- HTML5 / CSS3

## 📋 Pré‑requisitos

- Python 3.11 ou superior instalado
- Git (para clonar o repositório)
- Terminal / PowerShell (Linux, macOS ou Windows)

## 🚀 Como executar o projeto do zero

### 1. Clonar o repositório
```bash
git clone https://github.com/xjhfsz/sicm_project.git
cd sicm

2. Criar e ativar ambiente virtual
Windows:

bash
python -m venv venv
venv\Scripts\activate
Linux / macOS:

bash
python3 -m venv venv
source venv/bin/activate

3. Instalar as dependências
bash
pip install -r requirements.txt
Se você não tem o requirements.txt, crie‑o com:

pip install django
pip freeze > requirements.txt

4. Configurar o banco de dados (SQLite)
python manage.py makemigrations
python manage.py migrate

5. (Opcional) Criar um superusuário para acessar o admin
python manage.py createsuperuser

6. Executar o servidor de desenvolvimento
python manage.py runserver
Acesse no navegador: http://127.0.0.1:8000/

🧑‍💻 Como usar
Morador:
Acesse Cadastrar e crie uma conta (informe unidade, nome, e‑mail, senha)
Faça login com usuário e senha
No painel, clique em Autorizar Visitante
Preencha nome do visitante e a data da visita
A autorização aparece no dashboard com status Ativa (se for hoje) ou Expirada
O porteiro verá o nome na tela da portaria apenas no dia marcado

Portaria (consulta – sem login):
Acesse diretamente a rota /portaria/ (link no menu superior)
O sistema lista todos os visitantes autorizados para o dia atual
Use o campo de busca para encontrar um visitante específico

Administração (opcional):
Acesse /admin/ com o superusuário criado.
Gerencie moradores, autorizações e visualize todos os registros.

📁 Estrutura de pastas (essencial)
text
sicm_project/
├── core/
│   ├── migrations/
│   ├── templates/          # todos os HTML do projeto
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── sicm/                   # configurações do projeto
│   ├── settings.py
│   └── urls.py
├── db.sqlite3
├── manage.py
└── requirements.txt


🔮 Melhorias futuras (pós‑MVP)
Registro de entrada efetiva (botão “registrar chegada” na portaria)
Envio de notificação por e‑mail / WhatsApp para o morador
Relatórios mensais para o síndico
Suporte a autorizações recorrentes (ex: diarista, prestador de serviço)
Migração para PostgreSQL e deploy em nuvem

👥 Autores
Bruno Rodrigues
Johnathan Fontinele
Disciplina: Prática Profissional Supervisionada – UEMA/ADS
Nota 2: MVP – Sistema de Autorização para Condomínio
