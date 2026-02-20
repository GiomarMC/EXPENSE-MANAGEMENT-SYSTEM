import django_filters
from apps.ventas.models import Venta


class VentaFilter(django_filters.FilterSet):
    fecha_desde = django_filters.DateFilter(
        field_name="fecha",
        lookup_expr="date__gte"
    )

    fecha_hasta = django_filters.DateFilter(
        field_name="fecha",
        lookup_expr="date__lte"
    )

    tienda = django_filters.NumberFilter(
        field_name="tienda_id"
    )

    trabajador = django_filters.CharFilter(
        field_name="usuario_tienda__usuario_id"
    )

    metodo_pago = django_filters.CharFilter(
        field_name="metodo_pago",
        lookup_expr="iexact"
    )

    es_credito = django_filters.BooleanFilter(
        field_name="es_credito"
    )

    class Meta:
        model = Venta
        fields = []
