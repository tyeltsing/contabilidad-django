from django.db import models
from obispado.plan_de_cuentas.models import CuentaNivel3

class AsientoContable(models.Model):
    debe = models.ManyToManyField(CuentaNivel3, through='AsientoDebeDetalle', related_name='CuentasDebe')
    haber = models.ManyToManyField(CuentaNivel3, through='AsientoHaberDetalle', related_name='CuentasHaber')
    comentario = models.CharField(max_length=100, null=True)

class AsientoDebeDetalle(models.Model):
    asiento = models.ForeignKey(AsientoContable)
    cuenta = models.ForeignKey(CuentaNivel3)
    monto = models.FloatField()

class AsientoHaberDetalle(models.Model):
    asiento = models.ForeignKey(AsientoContable)
    cuenta = models.ForeignKey(CuentaNivel3)
    monto = models.FloatField()
