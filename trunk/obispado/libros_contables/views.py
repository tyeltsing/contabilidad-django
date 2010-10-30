# Create your views here.
from django.shortcuts import render_to_response
from obispado.plan_de_cuentas.models import *
from obispado.aportantes.models import *
from obispado.libros_contables.models import *
from django.db.models import Q
import datetime, string
import time
from datetime import date

def cargar_asiento(request):
    if 'date1xx' in request.GET and request.GET['date1xx']:
        fe = request.GET['date1xx']
        fecha = time.strptime(str(fe), "%d/%m/%Y")
        fechaiso = time.strftime("%Y-%m-%d", fecha)
        com = request.GET['comentarios']
        cuentad=[]
        cuentah=[]
        montod=[]
        montoh=[]
        newasiento = AsientoContable(fecha = fechaiso, comentario = str(com))
        newasiento.save()
        cont = 0
        for i in range(1, 11):
            if 'cd'+str(i) in request.GET and request.GET['cd'+str(i)]:
                    cuentad.append(request.GET['cd'+str(i)])
                    cont = cont + 1
            if 'd'+str(i) in request.GET and request.GET['d'+str(i)]:
                    montod.append(request.GET['d'+str(i)])
            if 'ch'+str(i) in request.GET and request.GET['ch'+str(i)]:
                    cuentah.append(request.GET['ch'+str(i)])
            if 'h'+str(i) in request.GET and request.GET['h'+str(i)]:
                    montoh.append(request.GET['h'+str(i)])
        for i in range(0, cont):
            haber = AsientoHaberDetalle(asiento_id = newasiento.id, cuenta_id = int(cuentah[i]), monto = float(montoh[i]))
            haber.save()
            debe = AsientoDebeDetalle(asiento_id = newasiento.id, cuenta_id = int(cuentad[i]), monto = float(montod[i]))
            debe.save()
        cn3 = CuentaNivel3.objects.all()
        return render_to_response('asiento/asiento.html', {'cn3': cn3, 'msj':'Asiento Cargado Correctamente'})
    else:
        cn3 = CuentaNivel3.objects.all()
        return render_to_response('asiento/asiento.html', {'cn3': cn3})
    return render_to_response('asiento/asiento.html')