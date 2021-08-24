#from sacatuturno.sacatuturno.settings import SECRET_KEY
from django.contrib.auth.views import LoginView
from .forms import formularioUser
from django.shortcuts import get_object_or_404, render, redirect
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
        form = formularioUser()    
     
    context = {
        'form': form
    }   
    return render(request,'registrarusuario.html', context)


def perfil(request):
    return render(request,'perfil.html', {})


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
