from django.contrib import admin
from .models import *
# Register your models here.
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "id" )

class ServicioPrestadoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "id", "descripcion")
class DiasAdmin(admin.ModelAdmin):
    list_display = ("day", "id")


class SubCategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "id", "categoria")

class TurnoAdmin(admin.ModelAdmin):
    list_display = ("id", "fecha_inicio")

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(ServicioPrestado, ServicioPrestadoAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Turno, TurnoAdmin)
admin.site.register(Days, DiasAdmin)