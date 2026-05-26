from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('registrar/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('morador/dashboard/', views.morador_dashboard, name='morador_dashboard'),
    path('morador/cadastrar_visitante/', views.cadastrar_visitante, name='cadastrar_visitante'),
    path('portaria/', views.portaria_lista, name='portaria_lista'),
]