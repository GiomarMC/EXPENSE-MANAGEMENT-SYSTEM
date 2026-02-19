from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, Asistencia, UsuarioTienda


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_active',
        'date_joined'
    )
    list_filter = (
        "is_staff",
        "is_active",
        "date_joined",
    )


@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    model = Rol
    list_display = ('id', 'nombre',)
    search_fields = ('nombre',)


class AsistenciaInline(admin.TabularInline):
    model = Asistencia
    extra = 0


@admin.register(UsuarioTienda)
class UsuarioTiendaAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tienda", "rol", "salario")
    list_filter = ("tienda", "rol")
    search_fields = ("usuario__username", "usuario__first_name",
                     "usuario__last_name")
    inlines = [AsistenciaInline]
