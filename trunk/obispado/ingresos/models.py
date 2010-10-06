from django.db import models
from obispado.aportantes.models import Aportante
from obispado.plan_de_cuentas.models import CuentaNivel3

# Create your models here.
class Venta(models.Model):
    fecha = models.DateTimeField()
    aportante = models.ForeignKey(Aportante)
    detalle = models.ManyToManyField(CuentaNivel3, through='VentaDetalle')
    
class VentaDetalle(models.Model):
    venta = models.ForeignKey(Venta)
    cuenta = models.ForeignKey(CuentaNivel3)
    gravadas5 = models.FloatField(null=True)
    gravadas10 = models.FloatField(null=True)
    iva5 = models.FloatField(null=True)
    iva10 = models.FloatField(null=True)
    exenta = models.FloatField(null=True)