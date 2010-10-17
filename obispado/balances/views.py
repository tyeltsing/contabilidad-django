from django.shortcuts import render_to_response, get_object_or_404
from obispado.libros_contables.models import *
from obispado.plan_de_cuentas.models import *

def index(request):
    # get_object_or_404(Poll, pk=poll_id)
    return render_to_response('balances/index.html')

def ver_balance(request):
    # TODO: Tema de las fechas, como hacer eso?
    # tal vez se podria pasar el parametro de mes, luego cuando se traen los
    # saldos de AsientoDebeDetalle y AsientoHaberDetalle filtrar por fecha,
    # usando filter (date <= fecha_que_me_paso_el_usuario)

    diccionario_balance = generar_balance(1, 2) # aca le paso dos enteros, pero 
                                                # deberian ser las fechas
    

import csv
from django.http import HttpResponse

def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=somefilename.csv'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response
