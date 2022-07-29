from django.db import models
from django.contrib.auth.models import User


# Sempre adicionar em admin.py do projeto
class Pacientes(models.Model):
    choices_sexo = (('F', 'Feminino'),
                    ('M', 'Maculino'))
    nome = models.CharField(max_length=50)
    sexo = models.CharField(max_length=1, choices=choices_sexo)
    idade = models.IntegerField()
    email = models.EmailField()
    telefone = models.CharField(max_length=19)
    nutri = models.ForeignKey(User, on_delete=models.CASCADE)  # Se a nutricionista excluir sua conta, seus pacientes serão excluidos | SET_NULL = paciente ficaria sem nutricionista

    def __str__(self):
        return self.nome


class DadosPaciente(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)  # CASCADE pois se o paciente for excluido, tds os dados deles sao tbm, pois aí n fica armazenando dados atoa
    data = models.DateTimeField()
    peso = models.IntegerField()
    altura = models.IntegerField()
    percentual_gordura = models.IntegerField()
    percentual_musculo = models.IntegerField()
    colesterol_hdl = models.IntegerField()
    colesterol_ldl = models.IntegerField()
    colesterol_total = models.IntegerField()
    trigliceridios = models.IntegerField()
    

    def __str__(self):
        return f"Paciente({self.paciente.nome}, {self.peso})"
    
    
class Refeicao(models.Model):
    paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    horario = models.TimeField()
    carboidratos = models.IntegerField()
    proteinas = models.IntegerField()
    gorduras = models.IntegerField()

    def __str__(self):
        return self.titulo


class Opcao(models.Model):
    refeicao = models.ForeignKey(Refeicao, on_delete=models.CASCADE)  # Ao excluir um paciente, as refeições dele tbm sao excluídas
    imagem = models.ImageField(upload_to="opcao")  # Vai ficar na pasta opção as imagens que a nutricionista enviar | Conforme está em setings do projeto  =  'media' por padrao /opcao/imagens de opcao de refeicao
    descricao = models.TextField()  # Sem limites de caracteres =  TextField
 
    def __str__(self):
        return self.descricao
    