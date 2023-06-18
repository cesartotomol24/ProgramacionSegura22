"""proyectoWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from proyectoWeb import views
urlpatterns = [
    path('login2/', views.login),
    path('servidor/', views.formulario_servidores),
    path('activo/', views.lista_servidores),
    path('ipcheck/', views.servidor_ip),
    path('monitoreo/', views.estado_servidor),
    #path('serializar_registros/',views.serializar_server),
    path('monitorizacion/',views.servicio_recuperar),
    path('apagar/',views.apagar_server),

]

