from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import os
import proyectoWeb.settings as conf
from bd import models
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime 

def monitoreo(request):
    t = 'monitoreo.html'
    if request.method == 'GET':
        return render(request, t)


def validar_servidores(hostname, direccion, contraseña):
    errores = []
    
    if not hostname:
        errores.append('El hostname está vacío')
    if not direccion:
        errores.append('La direccion esta vacia')
    if not contraseña.isnumeric():
        errores.append('La contraseña esta vacia')
    return errores




def formulario_servidores(request):
    t = 'formulario_servidores.html'
    if request.method == 'GET':
        return render(request, t)
    
    else:
        hostname = request.POST.get('hostname', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        contraseña = request.POST.get('password', '').strip()
        errores = validar_servidores(hostname, direccion, contraseña)
        
        if errores:
            c = {'errores': errores}
            return render(request, t, c)
        else:
            n_servidor = models.Servidor(hostname=hostname,
                                       direccionIP=direccion,
                                       password=contraseña)
            n_servidor.save()
            return redirect('/monitoreo/')



##Estado del Servidor 
def estado_servidor(request):
    t='monitoreo.html'
    d={'list':models.Servidor.objects.all()}
    return render(request,t,d)

###Actual en /monitoreo/
def lista_servidores(request):
    t='monitoreo.html'
    now = datetime.now()
    d={'list':models.Servidor.objects.all()}
    dir1 = servidor_ip(request)
    for server in models.Servidor.objects.all():
        if dir1 == server.direccionIP:
            print("Activo")
            print(dir1)
            print(server.direccionIP)
            server.estado = "Activo"
            hora = datetime.now()
            server.fecha = hora
            server.save()
        else :
            determinar_server(server)
                ahora = datetime.now()
                last_server = datetime.strptime(server.fecha, '%Y-%m-%d %H:%M:%S')
                """
	 	se transforma la variable fecha del servidor
		de regreso a tipo datetime para poder comparar segundos
                """
                dif = (ahora - last_server).total_seconds()
                """
		se comparan los segundos entre la
		última fecha del server y la actual
                """
                if dif > 60 :
                    print("servidor inactivo")
                    server.estado = "Indefinido"
                    server.save()
    return render(request,t,d)

            def determinar_server(server):
                ahora = datetime.now()
                last_server = datetime.strptime(server.fecha, '%Y-%m-%d %H:%M:%S')
                """
                se transforma la variable fecha del servidor
                de regreso a tipo datetime para poder comparar segundos
                """
                dif = (ahora - last_server).total_seconds()
                """
                se comparan los segundos entre la  
                última fecha del server y la actual
                """
                if dif > 60 :
                    print("servidor inactivo")
                    

def serializar_server(servidores):
    resultado = []
    for serv in servidores:
        d_server = {'Servidor':serv.hostname, 'DireccionIP' :serv.direccionIP, 'Estado': serv.estado, 'Fecha':serv.fecha}
        resultado.append(d_server)
    return resultado


def servicio_recuperar(request):
    """
    Servicio que actualiza.

    Keyword Arguments:
    request -- 
    returns: JsonResponse
    """
    servidores = models.Servidor.objects.all()
    return JsonResponse(serializar_server(servidores), safe=False)

##En /monito/
def comparar_IP(request):
    t='monitoreo.html'
    d={'list':models.Servidor.objects.all()}
    dir_sol = servidor_ip(request)
    for servidor in models.Servidor.objects.all() :
        if dir_sol == servidor.direccionIP :
            servidor.estado="Activo"
            servidor.save()
        else :
            servidor.estado="Indefinido"
            servidor.save()
    return render (request,t,d)


def servidor_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        #print(ip)
    else:
        ip = request.META.get('REMOTE_ADDR')
        #print(ip)
    #print(ip)
    return ip

