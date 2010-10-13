from django.shortcuts import render_to_response, get_object_or_404
from obispado.libros_contables.models import *

def index(request):
    # get_object_or_404(Poll, pk=poll_id)
    return render_to_response('balances/index.html')

#def ver_balance(request):
    # crearemos una lista con diccionario con el siguiente formato
    # lista_activos = [{cuenta:monto}]
    #activos = 
