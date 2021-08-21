from .forms import formularioUser
from django.shortcuts import render, redirect


# Create your views here.

def home(request):
    return render(request, 'home.html', {})


def crearcuenta(request):
    if request.method == 'POST':
        form = formularioUser(request.POST)
        if form.is_valid():
            form.save()           
            return redirect('perfil')     #si ingresa correctamente lo manda al perfil
    else:
        form = formularioUser()    
     
    context = {
        'form': form
    }   
    return render(request,'registrarusuario.html', context)



def perfil(request):
    return render(request,'perfil.html', {})