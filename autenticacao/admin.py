from django.contrib import admin
from .models import Ativacao  # tabela criada


admin.site.register(Ativacao)  # Aparecerá essa tabela no http://127.0.0.1:8000/admin
