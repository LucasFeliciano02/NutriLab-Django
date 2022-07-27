from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


# * Colocar o nome do app para que a url do projeto converse com a url do app 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('autenticacao.urls')),  # /auth Redireciona para o autenticacao.urls que tem a url cadastro/ que chama a view 'cadastro' que faz uma ação em views (tem que criar a url dentro do app, (nao cria automaticamente))
    path('', include('plataforma.urls'))  # Quando nao tem nada ele vai para as urls do app 'plataforma'
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
