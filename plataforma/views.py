from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages import constants
from .models import Pacientes, DadosPaciente, Refeicao, Opcao
from datetime import datetime


@login_required(login_url='/auth/logar/')  #* A função abaixo só pode ser acessado por usuários logados, se nao tiver, vai pra pg /logar/
def pacientes(request):
    if request.method == "GET":  # Se for fazer requisição 'GET', exibe o html 
        pacientes = Pacientes.objects.filter(nutri=request.user)   
        return render(request, 'pacientes.html', {'pacientes': pacientes})
    elif request.method == "POST":  # Se a requisição for 'POST', pega os dados que foram enviados atraves do <form> do paciennte.html
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')

        #* VERIFICAÇÕES E VALIDAÇÃO DE DADOS | strip = nao deixa enviar apenas espaços nos nomes
        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/pacientes/')

        if not idade.isnumeric():  # Não deixa que passe letras, pois a idade com o tipo 'number' pode ser alterado para 'text' no html do site ao ser inspecionado
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
            return redirect('/pacientes/')
        
        # Só pode ser cadastrado apenas um paciente com aquele e-mail, no caso o médio que faria isso e caso tentasse cadastrasse 1 pessoa já cadastrada com aquele email, daria erro 
        paciente = Pacientes.objects.filter(email=email)
        
        if paciente.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
            return redirect('/pacientes/')
                
        
        try:
            p1 = Pacientes(
                nome=nome,
                sexo=sexo,
                idade=idade,
                telefone=telefone,
                nutri=request.user,
            )
        
            p1.save()
            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso!')
            return redirect('/pacientes/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno no sistema')
            return redirect('/pacientes')


#* Dados do paciente

# busca os pacientes da nutricionista e envia os pacientes com suas caracteristicas
@login_required(login_url='/auth/logar/')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'dados_paciente_listar.html', {'pacientes': pacientes})
    

# Aparece os dados do paciente ao ser clicado
@login_required(login_url='/auth/logar/')
def dados_paciente(request, id):  # id que veio pela url
    paciente = get_object_or_404(Pacientes, id=id)  #  paciente = get_object_or_404.objects.get(id=id)   =    Busca no bd na tabela 'paciente' o paciente q foi clicado e isso ocorre pelo id
    if not paciente.nutri == request.user:  # Se a nutricionista desse paciente nao for igual a esse usuario q está logado, Nao deixa ela acessar seus dados
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')
    
    if request.method == "GET":    # .get traz apenas o único paciente clicado, assim nao precisa fazer o for, enquanto o .filter traz um lista de paciente
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'dados_paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})
    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')

        paciente = DadosPaciente(paciente=paciente,
                                data=datetime.now(),
                                peso=peso,
                                altura=altura,
                                percentual_gordura=gordura,
                                percentual_musculo=musculo,
                                colesterol_hdl=hdl,
                                colesterol_ldl=ldl,
                                colesterol_total=colesterol_total,
                                trigliceridios=triglicerídios)

        paciente.save()

        messages.add_message(request, constants.SUCCESS, 'Dados cadastrado com sucesso')
        
        return redirect('/dados_paciente/')
    
    
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/auth/logar/')
@csrf_exempt
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by("data")
    
    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos,
            'labels': labels}
    return JsonResponse(data) 


# Se tipo da requisição for "GET", ele lista tds os pacientes filtrando pelos pacientes dessa nutricionista em específico e envia esses dados para o html  "plano_alimentar_listar.html" q está em templates
def plano_alimentar_listar(request):
        if request.method == "GET":
            pacientes = Pacientes.objects.filter(nutri=request.user)
            return render(request, 'plano_alimentar_listar.html', {'pacientes': pacientes})


# Recebe requisição do usuario e id, há uma validação que caso o paciente nao seja da nutricionista, ele seja redirecionado para 'plano_alimentar_listar' 
def plano_alimentar(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/plano_alimentar_listar/')

    if request.method == "GET":  # Se o paciente for do nutricionista, é renderizado esse html e passa o paciente que com qual estamos trabalhando
        r1 = Refeicao.objects.filter(paciente=paciente).order_by("horario")  # Traga tds as refeições do bd em que o paciente seja igual ao paciente que estou acessando por horario
        opcao = Opcao.objects.all()
        return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao': r1, 'opcao': opcao})
    

def refeicao(request, id_paciente):  # Verifica se o paciente é da nutricionista msm
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/dados_paciente/')

    # Se o tipo da requisição for igual a "POST"(que veio pelo formulário), captura os dados abaixo
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')
        
        # Cria instancia de refeicao, confrme o que está em models
        r1 = Refeicao(paciente=paciente,
                      titulo=titulo,
                      horario=horario,
                      carboidratos=carboidratos,
                      proteinas=proteinas,
                      gorduras=gorduras)

        r1.save()  # Envia para o banco de dados de fato essas instancias

        messages.add_message(request, constants.SUCCESS, 'Refeição cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')  # Ao cadastrar a refeição, volta direto para o paciente que ja estava sendo trabalhado


def opcao(request, id_paciente):
    if request.method == "POST":  # pega o arquivo q tem o mesmo name="" que foi colocado no input do <html>
        id_refeicao = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem')  # Sempre quando for receber arquivos, se recebe atraves do FILES
        descricao = request.POST.get("descricao")

        o1 = Opcao(refeicao_id=id_refeicao,
                   imagem=imagem,  # models.ImageField(upload_to="opcao")  =  caminho para onde vai salvar as imagens
                   descricao=descricao)

        o1.save()

        messages.add_message(request, constants.SUCCESS, 'Opção cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')
