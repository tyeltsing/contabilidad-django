from django.db import models
from obispado.proveedores.models import Proveedor
from obispado.plan_de_cuentas.models import CuentaNivel3
from obispado.libros_contables.models import *

TIPO_COMPROBANTE_CHOICES = (
                     ('f', 'Factura'),
                     ('r', 'Recibo')
)

# Create your models here.
class Compra(models.Model):
    fecha = models.DateField()
    proveedor = models.ForeignKey(Proveedor)
    asiento = models.ForeignKey(AsientoContable, null=True)
    numero_comprobante = models.CharField(max_length=15)
    tipo_comprobante = models.CharField(max_length=1, choices=TIPO_COMPROBANTE_CHOICES)
    #detalle = models.ManyToManyField(CuentaNivel3, through='CompraDetalle')
    # UNIQUE TOGHETER, porque no puede repetirse la cuenta en el asiento
    class Meta:
        unique_together = (("proveedor", "numero_comprobante"),)
    
# class CompraDetalle(models.Model):
    # compra = models.ForeignKey(Compra)
    # cuenta = models.ForeignKey(CuentaNivel3)
    # gravadas5 = models.FloatField(null=True)
    # gravadas10 = models.FloatField(null=True)
    # iva5 = models.FloatField(null=True)
    # iva10 = models.FloatField(null=True)
    # exenta = models.FloatField(null=True)
    
    
def generar_resumen_egresos(fecha_desde, fecha_hasta):
    '''Genera el resumen para la planilla simplificada de egresos'''
    resultado = []
    # asi deberia quedar la planilla
    # nro_comprobante, fecha, tipo_factura_o_recibo(???? esto no esta en la BD!), identificador ruc o CI, nombre del proveedor, gravadas 10%, gravadas 5%, exentas, total iva incluido, iva10%, iva5%

    egresos = Compra.objects.filter(fecha__range=(fecha_desde, fecha_hasta)).order_by('fecha')
    for egreso in egresos:
        dic = {}
        dic['nro_comprobante'] = egreso.numero_comprobante
        dic['fecha'] = egreso.fecha
        dic['tipo_comprobante'] = 'factura' # wtf con esto
        dic['ruc_proveedor'] = egreso.proveedor.ruc
        dic['proveedor'] = egreso.proveedor.nombre
        #aqui me quede
    
    return resultado