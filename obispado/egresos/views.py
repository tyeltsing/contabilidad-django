# Create your views here.
from django.shortcuts import render_to_response
from obispado.egresos.models import *
from obispado.proveedores.models import *
from obispado.libros_contables.models import *
from obispado.plan_de_cuentas.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q, Max, Min
import datetime, string
import time
from datetime import date
import csv

def sumar(x, y):
    return x + y

def carga(request):
    if 'pro' in request.GET and request.GET['pro']:
        pro = request.GET['pro']
        fe = request.GET['date1xx']
        fecha = time.strptime(str(fe), "%d/%m/%Y")
        fechaiso = time.strftime("%Y-%m-%d", fecha)
        if 'ruc' in request.GET and request.GET['ruc']:
            ruc = request.GET['ruc']
        nrofac = request.GET['nrofac']
        if 'tot' in request.GET and request.GET['tot']:
            tot = request.GET['tot']
        tipodoc = request.GET['tipodoc']
        #else:
        #    tot = 1000
            
        id_proveedor = Proveedor.objects.filter(nombre=pro)
        valormaximo = Proveedor.objects.aggregate(Max('id'))
        valapmax = valormaximo['id__max']
        if valapmax:
            valapmax = valapmax + 1
        else:
            valapmax = 1
        newasiento = AsientoContable(fecha = fechaiso)
        newasiento.save()
        tipo_doc_str = ''
        if tipodoc == 1:
            tipo_doc_str = 'f'
        else if tipodoc == 2:
            tipo_doc_str = 'r'
        else if tipodoc == 3:
            tipo_doc_str = 'a'
        newingreso = Compra(fecha = fechaiso, proveedor_id = pro, numero_comprobante = nrofac, asiento = newasiento, tipo_comprobante=tipo_doc_str)
        newingreso.save()
        #newasiento.comentario = "egreso: " + str(newingreso.id))
        #newasiento.save()
        listcant = []
        listdes = []
        listpu = []
        lismon = []
        totiva = []
        g10 = []
        g5 = []
        listex = []
        cont = 0
        pos=-1
        for i in range(1, 11):
            if 'cant'+str(i) in request.GET and request.GET['cant'+str(i)]:
                listcant.append(request.GET['cant'+str(i)])
                cont = cont + 1
            else:
                listcant.append('0')
            if 'des'+str(i) in request.GET and request.GET['des'+str(i)]:
                listdes.append(request.GET['des'+str(i)])
            else:
                listdes.append('0')
            if 'pu'+str(i) in request.GET and request.GET['pu'+str(i)]:
                listpu.append(request.GET['pu'+str(i)])
            else:
                listpu.append('0')
            if 'mon'+str(i) in request.GET and request.GET['mon'+str(i)]:
                lismon.append(request.GET['mon'+str(i)])
            else:
                lismon.append('0')
            if 'totiva'+str(i) in request.GET and request.GET['totiva'+str(i)]:
                totiva.append(request.GET['totiva'+str(i)])
            else:
                totiva.append('0')
            if 'g10'+str(i) in request.GET and request.GET['g10'+str(i)]:
                g10.append(request.GET['g10'+str(i)])
            else:
                g10.append('0')
            if 'g5'+str(i) in request.GET and request.GET['g5'+str(i)]:
                g5.append(request.GET['g5'+str(i)])
            else:
                g5.append('0')
            if 'ex'+str(i) in request.GET and request.GET['ex'+str(i)]:
                listex.append(request.GET['ex'+str(i)])
            else:
                listex.append('0')
        totivat = 0
        totgv10 = 0
        totgv5 = 0
        totex = 0
        totgral = 0
        if 'totivah' in request.GET and request.GET['totivah']:
            totivat = request.GET['totivah']
        if 'totgv10h' in request.GET and request.GET['totgv10h']:
            totgv10 = request.GET['totgv10h']
        if 'totgv5h' in request.GET and request.GET['totgv5h']:
            totgv5 = request.GET['totgv5h']
        if 'totexh' in request.GET and request.GET['totexh']:
            totex = request.GET['totexh']
        #if 'totgralh' in request.GET and request.GET['totgralh']:
        totgral = request.GET['totgralh']
        #else:
        #    totgral = 555;
        listipos = []
        
        for i in range(0, cont):
            tipos_iva = CuentaNivel3.objects.get(id=listdes[i])
            if(tipos_iva.tipo_de_iva == 'd'):
                listipos.append('d')
            if(tipos_iva.tipo_de_iva == 'c'):
                listipos.append('c')
            if(tipos_iva.tipo_de_iva == 'e'):
                listipos.append('e')
        summonto = 0
        for i in range(0, cont):
            if(listipos[i] == 'd'):
                # traemos la cuenta iva 10 %
                cuenta_iva = CuentaNivel3.objects.get(nombre="IVA 10% Credito")
                # cargamos la gravada
                newventaasiento = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(listdes[i]), monto = g10[i])
                newventaasiento.save()
                # calculamos el iva y cargamos
                monto_iva = float(totiva[i]) - float(g10[i])
                newivadebe = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(cuenta_iva.id), monto = monto_iva)
                newivadebe.save()
            elif(listipos[i] == 'c'):
                # traemos la cuenta iva 5 %
                cuenta_iva = CuentaNivel3.objects.get(nombre="IVA 5% Credito")
                # cargamos la gravada
                newventaasiento = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(listdes[i]), monto = g5[i])
                newventaasiento.save()
                # calculamos el iva y cargamos
                monto_iva = float(totiva[i]) - float(g5[i])
                newivadebe = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(cuenta_iva.id), monto = monto_iva)
                newivadebe.save()
            elif(listipos[i] == 'e'):
                newventaasiento = AsientoDebeDetalle(asiento_id = int(newasiento.id), cuenta_id = int(listdes[i]), monto = listex[i])
                newventaasiento.save()
            
            # = summonto + int(listex[i])
        summonto = reduce(sumar, listex)
        #Cambiar a "Caja"
        id_de_cuenta = CuentaNivel3.objects.get(nombre="Caja")
        newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id =id_de_cuenta.id, monto = float(totgral))
        #newventaasiento = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id =1, monto = int(totgral))
        newventaasiento.save()
        nuevoidasiento = Compra.objects.get(id=newingreso.id)
        nuevoidasiento.asiento_id = newasiento.id
        nuevoidasiento.save()
        #return render_to_response('ingresos/carga_ingreso.html')
        #return HttpResponseRedirect('/carga_ingresos/')
        #return render_to_response('egresos/carga_egreso.html')
        pro = Proveedor.objects.all().order_by("id")
        con = CuentaNivel3.objects.all().order_by("id")
        return render_to_response('egresos/carga_egreso.html', {'pro': pro, 'con':con, 'msj': 'Egreso Agregado Correctamente'})
        #return render_to_response('principal/index.html', {'final': listex})
        #return HttpResponseRedirect('/carga_egresos/')
    else:
        pro = Proveedor.objects.all().order_by("id")
        con = CuentaNivel3.objects.all().order_by("id")
        return render_to_response('egresos/carga_egreso.html', {'pro': pro, 'con':con})
    return render_to_response('egresos/carga_egreso.html')

def solicitar_planilla_egresos(request):
    '''Solo muestra el template para pedir el csv'''
    return render_to_response('egresos/solicitar_planilla_egresos.html')

def generar_planilla_csv_egresos(request):
    '''Genera el csv, pero usa un metodo del modelo'''
    # dp vemos el parseo de fechas con Lore "javascript html css" Figueredo
    # mientras esto para probar
    print 'funciona?'
    print request.GET['fecha_inicio']
    print request.GET['fecha_fin']
    fecha_inicio = date(2010, 1, 31) # quitar dp
    fecha_fin = date.today() # quitar dp
    # aqui pedimos los datos del egreso
    datos_egresos = generar_resumen_egresos(fecha_inicio, fecha_fin)

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=planila_egresos.csv'

    writer = csv.writer(response)
    
    writer.writerow(['', '', 'Egresos']) # titulo
    # le dejo muchas lineas en blanco para que escriban lo que quieran
    writer.writerow([]) # linea en blanco
    writer.writerow([]) # linea en blanco
    writer.writerow([]) # linea en blanco
    writer.writerow([]) # linea en blanco
    writer.writerow([]) # linea en blanco
    # escribimos las columnas
    writer.writerow(['', '', 'Numero', 'Fecha', 'Tipo', 'Identificador RUC o C.I.', 'Nombre del Proveedor', 'Gravadas 10%', 'Gravadas 5%', 'Exentas', 'Total Iva Incluido', 'Tasa 10%', 'Tasa 5%'])
    for egreso in datos_egresos:
        writer.writerow(['', '', str(egreso['nro_comprobante']), str(egreso['fecha']), str(egreso['tipo_comprobante']), str(egreso['ruc_proveedor']), str(egreso['proveedor']), str(egreso['gravadas10']), str(egreso['gravadas5']), str(egreso['exentas']), str(egreso['total']), str(egreso['iva10']), str(egreso['iva5'])])
    
    return response
