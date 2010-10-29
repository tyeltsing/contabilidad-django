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
        id_de_cuenta = CuentaNivel3.objects.filter(nombre="Caja")
        cue = id_de_cuenta.count()
        newventaasiento = AsientoDebeDetalle(asiento_id = newasiento.id, cuenta_id =1, monto = summonto)
        newventaasiento.save()
        nuevoidasiento = Venta.objects.get(id=newingreso.id)
        nuevoidasiento.asiento_id = newasiento.id
        nuevoidasiento.save()
        #return render_to_response('ingresos/carga_ingreso.html')
        #Ventas.objects.get(id=request.GET['ap']).delete()
        return HttpResponseRedirect('/carga_ingresos/')
        #return render_to_response('ingresos/carga_ingreso.html', {'msj': fechaiso})
        #return render_to_response('ingresos/index.html', {'final': summonto})
    else:
        apo = Aportante.objects.all().order_by("id")
        con = CuentaNivel3.objects.all().order_by("id")
        return render_to_response('ingresos/carga_ingreso.html', {'apo': apo, 'con':con})
    return render_to_response('ingresos/carga_ingreso.html')
    
    
def carga_ingresos(request):
    
    return render_to_response('ingresos/carga_ingreso.html')