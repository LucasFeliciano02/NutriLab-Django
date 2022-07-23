from django.db import models
from django.contrib.auth.models import User


# Sempre que for mudar algo no bd, criar nova tabela, tem que fazer makemigrations 

# 1º  ao criar a classe do bd aqui em models, vai aparecer o initial em migrations, ai fazer as migrações e cadastrar em admia
# 2º  py manage.py makemigrations  =  Vai pegar tds as alterações nas models e criar um arquivo 'initials' em migrations
# 3º  py manage.py migrate  =  Agora sim as informações vao para o bd  
# 4º  A tabela nova criada nao aparecerá no admin/, entao tem que cadastrar no admin.py do app autenticacao


class Ativacao(models.Model):
    token = models.CharField(max_length=64)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ativo = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
