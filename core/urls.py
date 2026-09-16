from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cadastro/', views.cadastrar_morador, name='cadastro'),
    path('login/', views.logar_morador, name='login'),
    path('logout/', views.deslogar_morador, name='logout'),
    path('dashboard/', views.dashboard_morador, name='dashboard'),
    path('portaria/', views.portaria_lista, name='portaria'),
    path('api/visitantes/', views.listar_criar_visitantes, name='api_visitantes'),
    path('api/visitantes/<int:visitante_id>/revogar/', views.revogar_visitante, name='api_revogar_visitante'),
]