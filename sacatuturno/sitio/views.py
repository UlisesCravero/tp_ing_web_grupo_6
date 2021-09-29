#from sacatuturno.sacatuturno.settings import SECRET_KEY
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
from django.contrib.auth import authenticate
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.db.models import Q
import secrets

# Create your views here.



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
            email_body = "Hola %s, Gracias por registrarte. Para activar tu cuenta da clíck en este link en menos de 48 horas: http://127.0.0.1:8000/accounts/confirm/%s" % (username, activation_key)

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





def perfil(request, id):
    servicios = ServicioPrestado.objects.filter(propietario__id = id)
    return render(request,'perfil.html', {'servicios': servicios})





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
    return render(request, 'categorias.html', {'categorias': categorias})





def subcategoria(request, id):
    subcategoria = SubCategoria.objects.filter(categoria_id = id)
    return render(request, 'subcategoria.html', {'subcategoria': subcategoria})




def registrarservicio(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        form = formularioProfesional(request.POST)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.propietario_id = request.user.id
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
            turno.cliente_id = id_user
            turno.servicio_id = servicio_id
            turno.save()
            return HttpResponseRedirect(reverse('perfil', kwargs={'id': id_user})) 
    else:
        form = formularioTurno()    
     
    context = {
        'form': form
    }   
    return render(request,'turno.html', context)

