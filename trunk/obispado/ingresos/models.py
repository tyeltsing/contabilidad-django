from django.db import models
from django.db.models import Sum
from obispado.aportantes.models import Aportante
from obispado.plan_de_cuentas.models import CuentaNivel3
from obispado.libros_contables.models import AsientoContable, AsientoDebeDetalle

# Create your models here.
class Venta(models.Model):
    fecha = models.DateField()
    aportante = models.ForeignKey(Aportante)
    numero_factura = models.CharField(max_length=15, unique=True)
    #detalle = models.ManyToManyField(CuentaNivel3, through='VentaDetalle')
    asiento = models.ForeignKey(AsientoContable, null=True)
    def __unicode__(self):
        return '%d' % (self.id)
    
# class VentaDetalle(models.Model):
    # venta = models.ForeignKey(Venta)
    # cuenta = models.ForeignKey(CuentaNivel3)
    # cantidad = models.IntegerField()
    # exenta = models.FloatField(null=True)

def generar_planilla_ingresos(fecha_desde, fecha_hasta):
    '''Genera la planilla de ingresos'''
    ventas = Venta.objects.filter(fecha__range=(fecha_desde, fecha_hasta))
    resultado = {}
    resultado['fecha_desde'] = fecha_desde
    resultado['fecha_hasta'] = fecha_hasta
    resultado['ingresos'] = []
    for v in ventas:
        mini_dic = {}
        mini_dic['nro_factura'] = v.numero_factura
        mini_dic['fecha'] = v.fecha
        mini_dic['tipo'] = 'Factura'
        mini_dic['id_ruc'] = v.aportante.ruc
        mini_dic['nombre_aportante'] = v.aportante.nombre
        mini_dic['concepto'] = 'y que pasa si hay mas de un concepto'
        mini_dic['cantidad'] = '1' # esto no me parece bien, parece que VentaDetalle debe aparecer de nuevo
        mini_dic['tipo'] = 'Efectivo'
        mini_dic['total_iva_incluido'] = ''
        monto = AsientoHaberDetallle.objects.filter(asiento = v).aggregate(suma=Sum('monto'))
        mini_dic['total_exentas'] = str(monto['suma'])
        resultado['ingresos'].append(mini_dic)
    return resultado