#from sacatuturno.sacatuturno.settings import SECRET_KEY
from re import X
from django.contrib.auth.views import LoginView
from .forms import *
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from django.template.context_processors import csrf
from sitio.forms import *
from sitio.models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseNotFound
from django.contrib.auth import authenticate
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.db.models import Q
import secrets
import json
from types import SimpleNamespace

# Create your views here.

# import ipdb; ipdb.set_trace(); para debuguear, n->avanzo, c->hasta el final


def home(request):
    return render(request, 'home.html', {})




def crearcuenta(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = formularioUser(request.POST)
        if form.is_valid():
            form.save()

            #todo lo nuevo para la validacion de email
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = secrets.token_hex(20)
            activation_key = salt+email
            key_expires = datetime.datetime.today() + datetime.timedelta(2)  

            #Obtener el nombre de usuario
            user=User.objects.get(username=username)

            # Crear el perfil del usuario                                                                                                                                 
            new_profile = UserProfile(user=user, activation_key=activation_key, 
                key_expires=key_expires)
            new_profile.save()

            # Enviar un email de confirmación
            email_subject = 'Confirmación de cuenta'
            email_body = "Hola %s, Gracias por registrarte. Para activar tu cuenta da clíck en este link en menos de 48 horas: http://sacatuturno.herokuapp.com/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'myemail@example.com', [email], fail_silently=False)
            return render(request, 'home.html', {'estadoActivacion': 'Proceso de registración correcto. Activa tu cuenta'})
        else:
            messages.error(request, form.errors)
    else:
        form = formularioUser() 
        messages.error(request, form.errors)
           
     
    context = {
        'form': form
    }   
    return render(request,'registrarusuario.html', context)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
    
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('home')            
        else:
            messages.error(request,'Error! Verificar si la cuenta no fue activada o bien el usuario y contraseña son incorrectos.')
            return redirect('login')
    
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})



def devolverNombreServicio(id):
    intid = int(id)
    return ServicioPrestado.objects.get(id = intid).nombre

def perfil(request, id):
    servicios = ServicioPrestado.objects.filter(propietario__id = id)
    turnos = Turno.objects.filter(cliente__id = id)
    # Parse JSON into an object with attributes corresponding to dict keys.
    #import ipdb; ipdb.set_trace();
    turnosResponse = []
    for turno in turnos:
        turnosResponse.append({ 
            'nombreServicio':turno.servicio.nombre, 
            'fecha_inicio': turno.fecha_inicio.strftime("%Y-%m-%dT%H:%M:%S"),
            'fecha_fin' : turno.fecha_fin.strftime("%Y-%m-%dT%H:%M:%S"),
            'confirmado': turno.confirmado,
        })
    context = {
        'servicios': servicios,
        'turnos': json.dumps(turnosResponse)
    }
    return render(request,'perfil.html', context)


def paginaprivada(request):
    return render(request,'paginaprivada.html', {})


def register_confirm(request, activation_key):
    # Verifica que el usuario ya está logeado
    if request.user and request.user.is_authenticated:
        HttpResponseRedirect('home')

    # Verifica que el token de activación sea válido y sino retorna un 404
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
    if user_profile.key_expires < timezone.now():
        context = {
        'estadoActivacion': 'El token ha expirado. Debe completar el registro nuevamente'
        } 
        return render(request, 'home.html', context)
    # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
    user = user_profile.user
    user.is_active = True
    user.save()
    form = formularioUser()
    context = {
        'estadoActivacion': 'Activación completada. Ya puede loguearse correctamente'
    } 
    return render(request, 'home.html', context)   


def categorias(request):
    categorias = Categoria.objects.all()
    servicios = ServicioPrestado.objects.all()
    query = request.GET.get('buscar_servicio')

    if query:
        servicios = servicios.filter(
                Q(propietario__first_name__icontains=query) |
                Q(propietario__last_name__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(nombre__icontains=query)

            ).distinct()
    return render(request, 'categorias.html', {'categorias': categorias, 'servicios': servicios})

def categorias_filtro(request, id_subcategoria=None, ciudad=None):
    categorias = Categoria.objects.all()
    #subcategoria = SubCategoria.objects.all()
    
    if id_subcategoria:
       subcategoria = SubCategoria.objects.get(id = id_subcategoria)
    
    #import ipdb; ipdb.set_trace();

    if id_subcategoria != None and ciudad == None: 
        servicios = ServicioPrestado.objects.filter(subcategoria_id = id_subcategoria)
    elif id_subcategoria == None and ciudad != None: 
        servicios = ServicioPrestado.objects.filter(ciudad = ciudad)  
    else:
        servicios = ServicioPrestado.objects.filter(subcategoria_id = id_subcategoria, ciudad = ciudad)  

    query = request.GET.get('buscar_servicio')

    if query:
        servicios = servicios.filter(
                Q(propietario__first_name__icontains=query) |
                Q(propietario__last_name__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(nombre__icontains=query) |
                Q(ciudad__icontains =query)

            ).distinct()
    
    context = {
        'categorias': categorias,
        'servicios': servicios,
    }

    if id_subcategoria:
        context['subcategoria'] = subcategoria
    
   
    return render(request, 'categorias.html', context)


def subcategoria(request, id):
    subcategoria = SubCategoria.objects.filter(categoria_id = id)
    return render(request, 'subcategoria.html', {'subcategoria': subcategoria})

def agenda(request, servicio_id):
    
    servicio = ServicioPrestado.objects.get(id = servicio_id)
    if servicio.propietario.id != request.user.id:
        return HttpResponseNotFound()
    turnos = Turno.objects.filter(servicio__id = servicio_id)
   
    turnosResponse = []
    for turno in turnos:
        
        if turno.confirmado:
            turno_json = { 
                'nombreServicio':turno.servicio.nombre,            
                'fecha_inicio':turno.fecha_inicio.strftime("%Y-%m-%dT%H:%M:%S"),
                'fecha_fin' : turno.fecha_fin.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            
            if turno.cliente == None:
                turno_json['cliente'] = turno.cliente_aux
            else:
                turno_json['cliente'] = turno.cliente.first_name + ' ' +  turno.cliente.last_name

            turnosResponse.append(turno_json)
    turnosSinConfirmar = turnos.exclude(confirmado = True)

    context = {
        'turnos_sin_confirmar': turnosSinConfirmar,
        'turnos': json.dumps(turnosResponse),
        'id_servicio': servicio_id,
        'servicio': servicio,
    }
    return render(request, 'agenda.html', context)

def cambiar_estado_turno(request, id_servicio, id_turno, status):
    turno = Turno.objects.get(id = id_turno)
    if status == 1:
        #import ipdb; ipdb.set_trace();
        email = turno.cliente.email
        username = turno.cliente.username
        id_cli = turno.cliente.id
        turno.confirmado = True
        turno.save()
        email_subject = 'Turno confirmado'
        email_body = "Hola %s, su turno fue confirmado. Muchas gracias por utilizar nuestro sitio. Para ver su agenda ingrese: http://sacatuturno.herokuapp.com/perfil/%s" % (username, id_cli)
        send_mail(email_subject, email_body, None, [email], fail_silently=False)
    else:
        email = turno.cliente.email
        username = turno.cliente.username
        id_cli = turno.cliente.id
        email = turno.cliente.email
        email_subject = 'Turno cancelado'
        email_body = "Hola %s, su turno fue cancelado. Muchas gracias por utilizar nuestro sitio. Para ver su agenda ingrese: http://sacatuturno.herokuapp.com/perfil/%s" % (username, id_cli)
        send_mail(email_subject, email_body, None, [email], fail_silently=False)
        turno.delete()
    return HttpResponseRedirect(reverse('agenda', kwargs={'servicio_id': id_servicio}))


def registrarservicio(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = formularioProfesional(request.POST)
        #import ipdb; ipdb.set_trace();
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.propietario_id = request.user.id
            servicio.save()
            dias = form.cleaned_data['diasAtencion']
            for dia in dias:
                servicio.diasAtencion.add(dia) 
            servicio.save()
            return render(request, 'home.html', {'estadoServicio': 'Proceso de alta correcto'})   
    else:
        form = formularioProfesional()    
     
    context = {
        'form': form
    }   
    return render(request,'registrarservicio.html', context)


#cambiar nombre
def servicios(request, id_subcategoria):
    #import ipdb; ipdb.set_trace();
    servicios = ServicioPrestado.objects.filter(subcategoria_id = id_subcategoria)

    query = request.GET.get('buscar_servicio')

    if query:
        servicios = servicios.filter(
                Q(propietario__first_name__icontains=query) |
                Q(propietario__last_name__icontains=query) |
                Q(descripcion__icontains=query) |
                Q(nombre__icontains=query)

            ).distinct()
    return render(request, 'servicios.html', {'servicios': servicios})


def eliminar_servicio(request, id, id_user):
    servicio = ServicioPrestado.objects.get(id=id).delete()
    return HttpResponseRedirect(reverse('perfil', kwargs={'id': id_user}))



def editar_servicio(request, servicio_id, id_user):
    instance = ServicioPrestado.objects.get(id= servicio_id)
    form = formularioProfesional(request.POST or None, instance=instance)
    if request.method == 'POST':              
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('perfil', kwargs={'id': id_user}))
        else:
            messages.error(request, form.errors)                
     
    context = {
        'form': form,
        'servicio': instance
    }   
    return render(request,'registrarservicio.html', context)


#API para traer las subcategorias de una categoria
def traerSubcategorias(request, id_categoria):
    categoria = Categoria.objects.get(id = id_categoria)
    subcategorias = serializers.serialize('json', categoria.traerSubcategorias.all())
    return HttpResponse(subcategorias, content_type='application/json')



def pedir_turno(request, servicio_id, id_user):   
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        
        form = formularioTurno(request.POST)             
        if form.is_valid():           
            turno = form.save(commit=False) 
            servicio = ServicioPrestado.objects.get(id = servicio_id)
            id_propietario = servicio.propietario.id
            if request.user.id != servicio.propietario.id:
                turno.cliente_id = request.user.id
            else:
                #turno.cliente_aux = form.cliente_aux
                turno.confirmado = True
                turno.cliente = None
                                  
            turno.servicio_id = servicio_id          
            turno.fecha_inicio = datetime.datetime(turno.fecha_inicio.year, 
                                                   turno.fecha_inicio.month, 
                                                   turno.fecha_inicio.day, 
                                                   turno.horario.hour, 
                                                   turno.horario.minute,
                                                   0)

            fecha_aux = turno.fecha_inicio
            fecha_aux = fecha_aux + datetime.timedelta(minutes= turno.servicio.duracionTurno)
            turno.fecha_fin = fecha_aux            
            turno.save()
            if turno.cliente == None:
                messages.success(request, 'Turno creado con éxito!')
                return HttpResponseRedirect(reverse('agenda', kwargs={'servicio_id': turno.servicio_id}))
            else:
                messages.success(request, 'Turno creado con éxito! Recibirá un mail cuando sea confirmado.')
                return HttpResponseRedirect(reverse('perfil', kwargs={'id': request.user.id}))

    else:
        #import ipdb; ipdb.set_trace();
        servicio = ServicioPrestado.objects.get(id = servicio_id)
        id_propietario = servicio.propietario.id
        horarios = []
        for hora in servicio.listaHorarios:            
            horarios.append({ 
                'Hora': hora.strftime("%H:%M")                         
            })

        #import ipdb; ipdb.set_trace();              
        form = formularioTurno()
        
        turnos = serializers.serialize('json', Turno.objects.filter(servicio__id = servicio_id))    

    context = {
        'form': form,
        'turnos': turnos,
        'horarios': json.dumps(horarios),
        'id_propietario': id_propietario,
        'servicio': servicio,
    }   
    return render(request,'turno.html', context)

def robots_txt(request):
    return render(request, "robots.txt", {})