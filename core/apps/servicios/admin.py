from django.contrib import admin
from .models import Servicio


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = (
        "tienda",
        "usuario_tienda",
        "fecha_inicio",
        "fecha_fin",
        "costo",
        "es_credito"
    )
    list_filter = (
        "tienda",
        "es_credito"
    )
