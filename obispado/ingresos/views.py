# Create your views here.
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from obispado.ingresos.models import *
from obispado.aportantes.models import *
from obispado.libros_contables.models import *
from obispado.plan_de_cuentas.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q, Max, Min
import datetime, string
import time
from datetime import date

from django.template import RequestContext

def index(request):
    lista_ultimos_ingresos = Venta.objects.all().order_by('-fecha')[:5]
    return render_to_response('ingresos/index.html', {'lista_ultimos_ingresos': lista_ultimos_ingresos})

def sumar(x, y):
    return x + y    

def carga(request):
    if 'ap' in request.GET and request.GET['ap']:
        #d = request.GET['des1']
        ap = request.GET['ap']
        fe = request.GET['date1xx']
        fecha = time.strptime(str(fe), "%d/%m/%Y")
        fechaiso = time.strftime("%Y-%m-%d", fecha)
        #ruc = request.GET['ruc']
        nrofac = request.GET['nrofac']
        if 'tot' in request.GET and request.GET['tot']:
            tot = request.GET['tot']
        #else:
        #    tot = 1000
        #final = ap+fe+ruc+cant+des+pu+ex+tot
       
        id_aportante = Aportante.objects.filter(nombre=ap)
        valormaximo = Aportante.objects.aggregate(Max('id'))
        valapmax = valormaximo['id__max']
        if valapmax:
            valapmax = valapmax + 1
        else:
            valapmax = 1
        newingreso = Venta(fecha = fechaiso, aportante_id=ap, numero_factura=nrofac)
        newingreso.save()
        newasiento = AsientoContable(fecha = fechaiso, comentario = "ingreso: " + str(newingreso.id))
        newasiento.save()
        listcant = []
        listdes = []
        listpu = []
        listex = []
        cont = 0
        for i in range(1, 11):
            if 'cant'+str(i) in request.GET and request.GET['cant'+str(i)]:
                listcant.append(request.GET['cant'+str(i)])
                cont = cont + 1
            if 'des'+str(i) in request.GET and request.GET['des'+str(i)]:
                listdes.append(request.GET['des'+str(i)])
            if 'pu'+str(i) in request.GET and request.GET['pu'+str(i)]:
                listpu.append(request.GET['pu'+str(i)])
            if 'ex'+str(i) in request.GET and request.GET['ex'+str(i)]:
                listex.append(request.GET['ex'+str(i)])
            
        summonto = 0
        for i in range(0, cont):
            newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id = int(listdes[i]), monto = float(listex[i]))
            newventaasiento.save()
            summonto = summonto + float(listex[i])
        #summonto = reduce(sumar, listex)
        #Cambiar a "Caja"
        id_de_cuenta = CuentaNivel3.objects.get(nombre="Caja")
        cue = id_de_cuenta.count()
        newventaasiento = AsientoDebeDetalle(asiento_id = newasiento.id, cuenta_id =id_de_cuenta.id, monto = summonto)
        newventaasiento.save()
        nuevoidasiento = Venta.objects.get(id=newingreso.id)
        nuevoidasiento.asiento_id = newasiento.id
        nuevoidasiento.save()
        #return render_to_response('ingresos/carga_ingreso.html')
        #Ventas.objects.get(id=request.GET['ap']).delete()
        #return HttpResponseRedirect('/carga_ingresos/')
        apo = Aportante.objects.all().order_by("id")
        con = CuentaNivel3.objects.all().order_by("id")
        return render_to_response('ingresos/carga_ingreso.html', {'apo': apo, 'con':con, 'msj': 'Ingreso Agregado Correctamente'})
        #return render_to_response('ingresos/carga_ingreso.html', {'msj': fechaiso})
        #return render_to_response('ingresos/index.html', {'final': summonto})
    else:
        apo = Aportante.objects.all().order_by("id")
        con = CuentaNivel3.objects.all().order_by("id")
        return render_to_response('ingresos/carga_ingreso.html', {'apo': apo, 'con':con})
    return render_to_response('ingresos/carga_ingreso.html')
    
    
def carga_ingresos(request):
    
    return render_to_response('ingresos/carga_ingreso.html')


def solicitar_planilla_ingresos(request):
    '''Solo muestra el template para pedir el csv'''
    return render_to_response('egresos/solicitar_planilla_egresos.html')

def generar_planilla_csv_ingresos(request):
    '''Genera el csv, pero usa un metodo del modelo'''
    # dp vemos el parseo de fechas con Lore "javascript html css" Figueredo
    # mientras esto para probar
    print 'funciona?'
    print request.GET['fecha_inicio']
    print request.GET['fecha_fin']
    fecha_inicio = date(2010, 1, 31) # quitar dp
    fecha_fin = date.today() # quitar dp
    # aqui pedimos los datos del ingreso
    datos_ingresos = generar_resumen_ingresos(fecha_inicio, fecha_fin)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    # en el filename tal vez podriamos poner la fecha_inicio fecha_fin como parte del nombre
    response['Content-Disposition'] = 'attachment; filename=planila_ingresos.csv'

    writer = csv.writer(response)
    
    writer.writerow(['', '', 'ingresos']) # titulo
    # le dejo muchas lineas en blanco para que escriban lo que quieran
    writer.writerow([]) # linea en blanco
    writer.writerow([]) # linea en blanco
    writer.writerow([]) # linea en blanco
    writer.writerow([]) # linea en blanco
    writer.writerow([]) # linea en blanco
    # escribimos las columnas
    writer.writerow(['', '', 'Numero', 'Fecha', 'Tipo', 'Identificador RUC o C.I.', 'Nombre del Aportante', 'Concepto', 'Cantidad', 'Tipo', 'Total Iva Incluido', 'Total exentas', 'Gravadas 10%', 'Gravadas 5%'])
    for ingreso in datos_ingresos:
        writer.writerow(['', '', str(ingreso['nro_comprobante']), str(ingreso['fecha']), str(ingreso['tipo_comprobante']), str(ingreso['ruc_proveedor']), str(ingreso['proveedor']), str(ingreso['gravadas10']), str(ingreso['gravadas5']), str(ingreso['exentas']), str(ingreso['total']), str(ingreso['iva10']), str(ingreso['iva5'])])

    return response