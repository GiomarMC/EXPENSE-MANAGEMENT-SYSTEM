from django.contrib import admin
from .models import (
    CajaDiaria,
    Deuda,
    PagoDeuda,
    GastoFijo,
    GastoVariable

)



class PagoDeudaInline(admin.TabularInline):
    model = PagoDeuda
    extra = 0


@admin.register(CajaDiaria)
class CajaDiariaAdmin(admin.ModelAdmin):
    list_display = (
        "tienda",
        "usuario_tienda",
        "fecha_hora",
        "monto_esperado",
        "monto_real",
        "diferencia",
        "estado"
    )
    list_filter = (
        "tienda",
        "estado",
        "fecha_hora"
    )


@admin.register(GastoVariable)
class GastoVariableAdmin(admin.ModelAdmin):
    list_display = (
        "tienda",
        "descripcion",
        "monto",
        "fecha"
    )
    list_filter = (
        "tienda",
        "fecha"
    )


@admin.register(GastoFijo)
class GastoFijoAdmin(admin.ModelAdmin):
    list_display = (
        "tienda",
        "descripcion",
        "monto",
        "dia_pago"
    )
    list_filter = (
        "tienda",
    )


@admin.register(Deuda)
class DeudaAdmin(admin.ModelAdmin):
    list_display = (
        "cliente",
        "venta",
        "monto_total",
        "saldo",
        "estado"
    )
    list_filter = ("estado",)
    inlines = [PagoDeudaInline]
