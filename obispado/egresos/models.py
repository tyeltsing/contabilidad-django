from django.db import models
from obispado.proveedores.models import Proveedor
from obispado.plan_de_cuentas.models import CuentaNivel3
from obispado.libros_contables.models import AsientoContable

# Create your models here.
class Compra(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedor)
    asiento = models.ForeignKey(AsientoContable, null=True)
    numero_factura = models.CharField(max_length=15)
    #detalle = models.ManyToManyField(CuentaNivel3, through='CompraDetalle')
    # UNIQUE TOGHETER, porque no puede repetirse la cuenta en el asiento
    class Meta:
        unique_together = (("proveedor", "numero_factura"),)
    
# class CompraDetalle(models.Model):
    # compra = models.ForeignKey(Compra)
    # cuenta = models.ForeignKey(CuentaNivel3)
    # gravadas5 = models.FloatField(null=True)
    # gravadas10 = models.FloatField(null=True)
    # iva5 = models.FloatField(null=True)
    # iva10 = models.FloatField(null=True)
    # exenta = models.FloatField(null=True)
    
    
