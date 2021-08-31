from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField
import datetime

# Create your models here.

tipo_user = [
    ('cliente', 'CLIENTE'),
    ('profesional', 'PROFESIONAL')
]

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    activation_key = models.CharField(max_length=255, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())
    tipo = models.CharField(max_length= 16, choices=tipo_user, verbose_name= 'Tipo usuario', null = True, default = 'cliente' )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'Perfiles de Usuario'


#categoria principal -> ej medicina, cuidado persona, etc.
class Categoria(models.Model):
    nombre = models.CharField(max_length=255, blank = False)

class SubCategoria(models.Model):
    nombre = models.CharField(max_length=255, blank = False)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

class ServicioPrestado(models.Model):
    nombre = models.CharField(max_length=255, blank = False)
    descripcion = models.CharField(max_length=255, blank = False)
    propietario = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    subcategoria = models.ForeignKey(SubCategoria, on_delete=models.CASCADE)
