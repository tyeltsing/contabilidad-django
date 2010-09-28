from django.db import models
from obispado.Proveedors.models import Proveedor
from obispado.plan_de_cuentas.models import CuentaNivel3

# Create your models here.
class Compra(models.Model):
	fecha = models.DateTimeField()
	Proveedor = models.ForeignKey(Proveedor)
	detalle = models.ManyToManyField(CuentaNivel3, through='CompraDetalle')
	
	
class CompraDetalle(models.Model):
	compra = models.ForeignKey(Compra)
	cuenta = models.ForeingKey(CuentaNivel3)
	gravadas5 = models.FloatField(null=True)
	gravadas10 = models.FloatField(null=True)
	iva5 = models.FloatField(null=True)
	iva10 = models.FloatField(null=True)
	exenta = models.FloatField(null=True)
	
	
