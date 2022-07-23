from django.urls import path  # Função do django que permite criar uma nova url
from . import views  # chamar a funcao que está em views


# Variável na qual preciso colocar minhas urls
urlpatterns = [
         #   URL,   |     FUNÇÃO,   |    NOME
    path('cadastro/', views.cadastro, name="cadastro"),
    path('logar/', views.logar, name="logar"),
    path('sair/', views.sair, name="sair"),
    path('ativar_conta/<str:token>/', views.ativar_conta, name="ativar_conta")
]        
