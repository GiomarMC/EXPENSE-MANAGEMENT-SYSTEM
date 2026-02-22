from django.db import transaction
from rest_framework.exceptions import ValidationError
from apps.finanzas.models.deudas import PagoDeuda


class DeudaService:

    @staticmethod
    @transaction.atomic
    def registrar_pago(deuda, monto):
        if deuda.estado == "PAGADA":
            raise ValidationError("La deuda ya esta pagada")

        if monto > deuda.saldo:
            raise ValidationError("El mondo excede el saldo")

        PagoDeuda.objects.create(
            deuda=deuda,
            monto=monto
        )

        deuda.saldo -= monto

        if deuda.saldo == 0:
            deuda.estado = "PAGADA"

        deuda.save(update_fields=["saldo", "estado"])

        return deuda
