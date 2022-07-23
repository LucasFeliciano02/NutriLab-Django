from django.shortcuts import render  # Renderiza uma pg html
from django.http import HttpResponse
from .utils import password_is_valid, email_html  # Função para senhas fortes em utils.py
from django.shortcuts import redirect, get_object_or_404  # Redirecionamento
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages  # Mensagens de erro que esta em settings.py
from django.contrib import auth
import os
from django.conf import settings
from .models import Ativacao
from hashlib import sha256  


# Sempre que o usuario acessa o site, ele envia uma request
def cadastro(request):  # Função cadastro recebe requisição do usuário e retorna uma msg Http
    if request.method == "GET":  # Se o metodo da requisição do usuario for get, renderiza o arquivo.html 
        if request.user.is_authenticated:  # Se o usuario estiver autenticado, ele é redirecionado para outra pg e nao pra de login, pois n pode ter  mais acesso a essas paginas
            return redirect('/')
        return render(request, 'cadastro.html')  # Retorna a requisição do usuário e o caminho do arquivo html
    elif request.method == "POST":  # Pegar dados que veio da requisição post
        username = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        
        if not password_is_valid(request, senha, confirmar_senha):
            return redirect('/auth/cadastro')  # Se os requisitos acima não forem válidos, ele retorna para refazer o cadastro na mesma página
        
        try:
            user = User.objects.create_user(username=username,
                                            password=senha,
                                            is_active=False)  # is_active=False Faz com que o usuario tenha que clicar em um link que sera enviado ao seu e-mail
            user.save()
            
            
            #* Token que ativa a conta
            
            token = sha256(f"{username}{email}".encode()).hexdigest()  # .encode() transfoma os dados em binário pois o sha256 precisa dos dados em binário para que consiga fazer a hash
            ativacao = Ativacao(token=token, user=user)
            ativacao.save()  # salva a ativacao no bd

            
            #* Depois que o usuário foi salvo no bd, chama uma função que envia o email 
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=username,  link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}") 
            
                        
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso')  # Requisição do usuario, tipo de mensagem.ERROR, 'mensagem'
            return redirect('/auth/logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')  # Requisição do usuario, tipo de mensagem.ERROR, 'mensagem'
            return redirect('/auth/cadastro')


def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:  # Se o usuario estiver autenticado, ele é redirecionado para outra pg e nao pra de login, pois n pode ter  mais acesso a essas paginas
            return redirect('/')
        return render(request, 'login.html')  # Se a requisição for GET, renderiza essa pagina html
    elif request.method == "POST":  # Se o usuario clicar no botao ele envia os dados para a url 'logar', conforme está em urls e colocar isso no action do form do html
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')
        
        usuario = auth.authenticate(username=username, password=senha)  # Verificar se existe um usuário no banco de dados que tem esse username e senha
        
        if not usuario:  # Se n existe nenhum usuario mostra a msg, no caso errar a digitação, ele redirecionar para logar, a msm página e tentar novamente
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/logar')
        else:  # Se JÁ existe o usuário, retorna para outra pg
            auth.login(request, usuario)
            return redirect('/pacientes')  #* Quando o usuario fizer login, ele é redirecionado para dentro do site e assim pode utilizar
        
        
def sair(request):
    auth.logout(request)
    return redirect('/auth/logar')


def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token)  # Pega o item do bd no qual o token é igual ao token que foi recebido na url, se nao encontrar o token, traz o erro 404
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Esse token já foi usado')
        return redirect('/auth/logar')
        
    user = User.objects.get(username=token.user.username)  # Se o token nao estiver ativo ele procura o usuario
    user.is_active = True  # alteracao de dado
    user.save()
    
    token.ativo = True  # o token fica inutilizavel depois de ter sido autenticado pelo usuário
    token.save()
    
    messages.add_message(request, constants.SUCCESS, 'Conta ativada com sucesso')
    return redirect('/auth/logar')
