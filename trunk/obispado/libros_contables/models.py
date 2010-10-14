from django.db import models
from obispado.plan_de_cuentas.models import CuentaNivel3

class AsientoContable(models.Model):
    fecha = models.DateField()
    debe = models.ManyToManyField(CuentaNivel3, through='AsientoDebeDetalle', related_name='CuentasDebe', null=True)
    haber = models.ManyToManyField(CuentaNivel3, through='AsientoHaberDetalle', related_name='CuentasHaber', null=True)
    comentario = models.CharField(max_length=100, null=True)

    def __unicode__(self):
        return str(self.fecha) + ' - #:' + str(self.id) + ' - ' + self.comentario

class AsientoDebeDetalle(models.Model):
    asiento = models.ForeignKey(AsientoContable)
    cuenta = models.ForeignKey(CuentaNivel3)
    monto = models.FloatField()
    # UNIQUE TOGHETER, porque no puede repetirse la cuenta en el asiento
    #class Meta:
    #    unique_together = (("asiento", "cuenta"),)

    def __unicode__(self):
        return str(self.asiento) + ' - ' + str(self.id)

class AsientoHaberDetalle(models.Model):
    asiento = models.ForeignKey(AsientoContable)
    cuenta = models.ForeignKey(CuentaNivel3)
    monto = models.FloatField()
    # UNIQUE TOGHETER, porque no puede repetirse la cuenta en el asiento
    #class Meta:
    #    unique_together = (("asiento", "cuenta"),)

    def __unicode__(self):
        return str(self.asiento) + ' - ' + str(self.id)