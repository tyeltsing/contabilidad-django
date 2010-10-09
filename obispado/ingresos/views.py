# Create your views here.
from django.shortcuts import render_to_response
from obispado.ingresos.models import *
from obispado.aportantes.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q, Max, Min

def index(request):
    lista_ultimos_ingresos = Venta.objects.all().order_by('-fecha')[:5]
    return render_to_response('ingresos/index.html', {'lista_ultimos_ingresos': lista_ultimos_ingresos})

def carga(request):
    if 'ap' in request.GET and request.GET['ap']:
        ap = request.GET['ap']
        fe = request.GET['fe']
        ruc = request.GET['ruc']
        cant = request.GET['cant']
        des = request.GET['des']
        pu = request.GET['pu']
        ex = request.GET['ex']
        if 'tot' in request.GET and request.GET['tot']:
            tot = request.GET['tot']
        else:
            tot = 1000
        #final = ap+fe+ruc+cant+des+pu+ex+tot
        id_aportante = Aportante.objects.filter(nombre=ap)
        valormaximo = Aportante.objects.aggregate(Max('id'))
        valapmax = valormaximo['id__max']
        valapmax = valapmax + 1
        newingreso = Venta(fecha = fe, aportante_id=1)
        newingreso.save()
        #return render_to_response('ingresos/carga_ingreso.html')
        return HttpResponseRedirect('/carga_ingresos/')
        #return render_to_response('ingresos/index.html', {'final': final})
    return render_to_response('ingresos/carga_ingreso.html')
    
def carga_ingresos(request):
    return render_to_response('ingresos/carga_ingreso.html')