from django.contrib import admin
from .models import Producto, Lote, LoteProducto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "is_active")
    search_fields = ("nombre",)


class LoteProductoInline(admin.TabularInline):
    model = LoteProducto
    extra = 1


@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "tienda",
        "fecha_llegada",
        "costo_operacion",
        "costo_transporte",
        "is_active"
    )
    list_filter = ("tienda", "fecha_llegada")
    inlines = [LoteProductoInline]


@admin.register(LoteProducto)
class LoteProductoAdmin(admin.ModelAdmin):
    list_display = (
        "lote",
        "producto",
        "cantidad_inicial",
        "cantidad_actual",
        "precio_compra",
        "precio_venta_base",
        "is_active"
    )
    list_filter = ("lote__tienda", "producto")
