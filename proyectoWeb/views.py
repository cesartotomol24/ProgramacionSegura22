from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import os
import proyectoWeb.settings as conf
from bd import models
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timezone

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
    d={'list':models.Servidor.objects.all()}
    dir1 = servidor_ip(request)
    estado = "Apagado"
    for server in models.Servidor.objects.all():
        if dir1 == server.direccionIP:
            print("Activo")
            print(dir1)
            print(server.direccionIP)
            server.estado = "Activo"
            server.fecha = datetime.now()
            server.save()
        else:
            determinar_server(server)
    return HttpResponse("Activo")


def determinar_server(server):
    ahora = datetime.now()
    dif = (ahora - server.fecha.replace(tzinfo=None))
    dif = dif.total_seconds()
    if server.estado != "Apagado":
        if dif > 20 :
            print("servidor inactivo")
            server.estado = "indefinido"
            server.save()


def apagar_server(request):
    dir = servidor_ip(request)
    for server in models.Servidor.objects.all():
        if dir == server.direccionIP:
            print("Apagado")
            server.estado = "Apagado"
            server.fecha = datetime.now()
            server.save()
    return HttpResponse("Apagado")




def serializar_server(servidores):
    resultado = []
    for serv in servidores:
        determinar_server(serv)
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


def validar_login(nombre,password):
    errores = []

    if not nombre:
        errores.append('El nombre está vacío')
    if not password.isnumeric():
        errores.append('La contraseña esta vacia')
    return errores


def loginAdmin(request):
    t = 'loginAdministrador.html'
    if request.method == 'GET':
        return render(request, t)
    
    else:
        nombre = request.POST.get('nombre', '').strip()
        password = request.POST.get('password', '').strip()
        errores = validar_login(nombre, password)
        
        if errores:
            c = {'errores': errores}
            return render(request, t, c)
        else:
            n_usuario = models.LoginAdmin(Nombre=nombre,Password=password)
            n_usuario.save()
            return redirect('/servidor/')



def credenciales(nombre,password):
    try:
        usuarios = models.LoginAdmin.objects.get(Nombre=nombre, Password=password)
        return True
    except:
        return False

def login(request):
    t = 'login.html'
    logueado = request.session.get('logueado', False)
    if request.method == 'GET':
       return render(request,t)
    elif request.method == 'POST':
        errores = []
        nombre = request.POST.get('nombre','')
        password =  request.POST.get('password','')
        if not nombre.strip() or not password.strip():
            errores.append('No se ingreso usuario o contraseña')
            return render(request,t,{'errores':errores})

        if not credenciales(nombre, password):
            errores.append('El usuario o contraseña son invalidos')
            return render(request,t,{'errores':errores})
        request.session['logueado']= True
        request.session['nombre']= nombre
        return redirect('/monitoreo/')
    

