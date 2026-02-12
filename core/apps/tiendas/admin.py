from django.contrib import admin
from .models import Tienda


@admin.register(Tienda)
class TiendaAdmin(admin.ModelAdmin):
    list_display = ("nombre_sede", "direccion", "id_duenio", "created_at")
    search_fields = ("nombre_sede", "direccion")
    list_filter = ("created_at",)
