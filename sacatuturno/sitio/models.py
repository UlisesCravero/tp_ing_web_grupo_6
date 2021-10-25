from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField
import datetime, time
from sitio import myFields

# Create your models here.

tipo_user = [
    ('cliente', 'CLIENTE'),
    ('profesional', 'PROFESIONAL')
]


ciudades = [
    ('Rafaela', 'Rafaela'),
    ('Santa Fe', 'Santa Fe'),
    ('Rosario', 'Rosario')
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    activation_key = models.CharField(max_length=255, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())
    tipo = models.CharField(max_length= 16, choices=tipo_user, verbose_name= 'Tipo usuario', null = True, default = 'cliente' )

    @property 
    def traerServicio(self):
        return ServicioPrestado.objects.filter(propietario__id = self.id)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'Perfiles de Usuario'




#categoria principal -> ej medicina, cuidado persona, etc.
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, blank = False)
    
    @property 
    def traerSubcategorias(self):
        return SubCategoria.objects.filter(categoria__id = self.id)
        
    def __str__(self):
        return self.nombre



class SubCategoria(models.Model):
    nombre = models.CharField(max_length=255, blank = False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nombre


class Days(models.Model):
    day = models.CharField(max_length=10)
    
    def __str__(self):
        return self.day

class ServicioPrestado(models.Model):
    nombre = models.CharField(max_length=50, blank = False)       # NO LLEVA NOMBRE EL SERVICIO PRESTADO
    descripcion = models.TextField(max_length=150, blank = False)
    propietario = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, blank = True, null= True)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE, blank = True, null= True)
    diasAtencion = models.ManyToManyField(Days)
    duracionTurno = models.IntegerField(default = 30, null= False, blank = False)
    ciudad = models.CharField(max_length= 20, choices = ciudades, verbose_name='Ciudad', blank = True, null= True, default = 'Rafaela')
    inicioJornada = models.TimeField( auto_now=False, auto_now_add=False, verbose_name="Inicio de Jornada",blank=True, null=False, default='08:00:00')
    finJornada = models.TimeField( auto_now=False, auto_now_add=False, verbose_name="Fin de Jornada",blank=True, null=False, default='17:00:00')

    @property 
    def listaHorarios(self):
        horarios=[]
        inicio = self.inicioJornada
        #import ipdb; ipdb.set_trace();
        horarios.append(inicio)       
        while inicio <= self.finJornada:
            
            fecha_aux= datetime.datetime(2021,1,1,inicio.hour,inicio.minute,0)
            fecha_aux = fecha_aux + datetime.timedelta(minutes= self.duracionTurno)
            inicio = datetime.time(fecha_aux.hour,fecha_aux.minute)
            horarios.append(inicio)

        #import ipdb; ipdb.set_trace();
        return horarios

    def __str__(self):
        return self.nombre



class Turno(models.Model):
    servicio = models.ForeignKey(ServicioPrestado, on_delete=models.CASCADE)
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    fecha_inicio = models.DateTimeField(verbose_name='Fecha inicio', default=datetime.datetime.today())
    horario = models.TimeField( auto_now=False, auto_now_add=False, verbose_name="Horario",blank=True, null=False, default='08:00:00')
    fecha_fin = models.DateTimeField(verbose_name='Fecha Fin',blank=True, null=True, default=datetime.datetime.today())
    confirmado = models.BooleanField( default=False)
    cliente_aux = models.TextField(max_length=50, blank = False, null=True)
    

