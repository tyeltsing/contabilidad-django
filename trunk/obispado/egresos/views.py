# Create your views here.
from django.shortcuts import render_to_response
from obispado.egresos.models import *
from obispado.proveedores.models import *
from obispado.libros_contables.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q, Max, Min
import datetime, string

def sumar(x, y):
    return x + y

def carga(request):
    if 'pro' in request.GET and request.GET['pro']:
        pro = request.GET['pro']
        fe = request.GET['fe']
        ruc = request.GET['ruc']
        nrofac = request.GET['nrofac']
        if 'tot' in request.GET and request.GET['tot']:
            tot = request.GET['tot']
        else:
            tot = 1000
            
        id_proveedor = Proveedor.objects.filter(nombre=pro)
        valormaximo = Proveedor.objects.aggregate(Max('id'))
        valapmax = valormaximo['id__max']
        if valapmax:
            valapmax = valapmax + 1
        else:
            valapmax = 1
        newingreso = Compra(fecha = fe, proveedor_id=pro, numero_factura=nrofac)
        newingreso.save()
        newasiento = AsientoContable(fecha = fe, comentario = "egreso: " + str(newingreso.id))
        newasiento.save()
        listcant = []
        listdes = []
        listpu = []
        lismon = []
        totiva = []
        g10 = []
        g5 = []
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
            if 'mon'+str(i) in request.GET and request.GET['mon'+str(i)]:
                lismon.append(request.GET['mon'+str(i)])
            if 'totiva'+str(i) in request.GET and request.GET['totiva'+str(i)]:
                totiva.append(request.GET['totiva'+str(i)])
            if 'g10'+str(i) in request.GET and request.GET['g10'+str(i)]:
                g10.append(request.GET['g10'+str(i)])
            if 'g5'+str(i) in request.GET and request.GET['g5'+str(i)]:
                g5.append(request.GET['g5'+str(i)])
            if 'ex'+str(i) in request.GET and request.GET['ex'+str(i)]:
                listex.append(request.GET['ex'+str(i)])
            
        summonto = 0
        for i in range(0, cont):
            newventaasiento = AsientoDebeDetalle(asiento_id = newasiento.id, cuenta_id = 1, monto = int(listex[i]))
            newventaasiento.save()
            
            # = summonto + int(listex[i])
        summonto = reduce(sumar, listex)
        #Cambiar a "Caja"
        id_de_cuenta = CuentaNivel3.objects.filter(nombre="Caja")
        newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id =1, monto = 1000)
        newventaasiento.save()
        nuevoidasiento = Compra.objects.get(id=newingreso.id)
        nuevoidasiento.asiento_id = newasiento.id
        nuevoidasiento.save()
        #return render_to_response('ingresos/carga_ingreso.html')
        #return HttpResponseRedirect('/carga_ingresos/')
        #return render_to_response('egresos/carga_egreso.html')
        return HttpResponseRedirect('/carga_egresos/')
    else:
        pro = Proveedor.objects.all().order_by("id")
        con = CuentaNivel3.objects.all().order_by("id")
        return render_to_response('egresos/carga_egreso.html', {'pro': pro, 'con':con})
    return render_to_response('egresos/carga_egreso.html')

