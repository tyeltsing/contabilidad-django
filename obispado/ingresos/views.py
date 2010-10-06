# Create your views here.
from django.shortcuts import render_to_response
from obispado.ingresos.models import *

def index(request):
    lista_ultimos_ingresos = Venta.objects.all().order_by('-fecha')[:5]
    return render_to_response('ingresos/index.html', {'lista_ultimos_ingresos': lista_ultimos_ingresos})

def carga(request):
    return render_to_response('ingresos/carga_ingreso.html')
    