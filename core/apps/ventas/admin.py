from django.contrib import admin
from .models import Venta, VentaProducto, Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "telefono",
    )
    search_fields = ("nombre", "telefono")


class VentaProductoInline(admin.TabularInline):
    model = VentaProducto
    extra = 1


@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tienda",
        "usuario_tienda",
        "fecha",
        "metodo_pago",
        "total",
        "es_credito"
    )
    list_filter = (
        "tienda",
        "metodo_pago",
        "es_credito",
        "fecha"
    )
    inlines = [VentaProductoInline]


@admin.register(VentaProducto)
class VentaProductoAdmin(admin.ModelAdmin):
    list_display = (
        "venta",
        "lote_producto",
        "cantidad",
        "precio_venta"
    )
    list_filter = ("lote_producto",)
