# Create your views here.
from django.shortcuts import render_to_response
from obispado.egresos.models import *
from obispado.proveedores.models import *
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q, Max, Min
import datetime, string

def carga(request):
    #if 'ap' in request.GET and request.GET['ap']:
    #    
    return render_to_response('egresos/carga_egreso.html')
    # Comente lo anterior porque me daba error nomas :)
