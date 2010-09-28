from django.db import models

# Create your models here.
class Venta(models.Model):
	fecha = models.DateTimeField()
	aportante = models.ForeignKey(Aportante)
	detalle = models.ManyToManyField(CuentaNivel3, through='VentaDetalle')
	
class VentaDetalle(models.Model):
	venta = models.ForeignKey(Venta)
	cuenta = models.ForeingKey(CuentaNivel3)
	gravadas5 = models.FloatField(null=True)
	gravadas10 = models.FloatField(null=True)
	iva5 = models.FloatField(null=True)
	iva10 = models.FloatField(null=True)
	exenta = models.FloatField(null=True)