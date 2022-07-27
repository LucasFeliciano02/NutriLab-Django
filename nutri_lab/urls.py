"""nutri_lab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
