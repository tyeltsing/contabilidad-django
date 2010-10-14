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

    grupos_de_cuentas = TipoCuenta.objects.all()
    diccionario_balance = {}

    grupos_de_cuentas = TipoCuenta.objects.all()
    diccionario_balance = {}
    # Disculpame Kreitmayr por la falta de recursividad en esta parte :)
    for g in grupos_de_cuentas:
        diccionario_balance[g] = {'suma': 0}
        lista_nivel1 = CuentaNivel1.objects.filter(tipo=g)
        for n1 in lista_nivel1:
            diccionario_balance[g][n1] = {'suma': 0}
            lista_nivel2 = CuentaNivel2.objects.filter(tipo=n1)
            for n2 in lista_nivel2:
                diccionario_balance[g][n1][n2] = {'suma': 0}
                lista_nivel3 = CuentaNivel3.objects.filter(tipo=n2)
                for n3 in lista_nivel3:
                    diccionario_balance[g][n1][n2][n3] = {'suma': 0}

    # ya tenemos la lista completa de cuentas, ahora debemos calcular el saldo a
    # la fecha del balance
    # recorremos nuestro super diccionario de la manera mas ineficaz
    for g in diccionario_balance:
        if g != 'suma':
            for n1 in diccionario_balance[g]:
                if n1 != 'suma':
                    for n2 in diccionario_balance[g][n1]:
                        if n2 != 'suma':
                            for n3 in diccionario_balance[g][n1][n2]:
                                if n3 != 'suma':
                                    saldo = 0
                                    lista_monto_debe_n3 = AsientoDebeDetalle.objects.filter(cuenta=n3)
                                    suma_monto_debe_n3 = 0
                                    for i in lista_monto_debe_n3:
                                        suma_monto_debe_n3 += i.monto
                                    lista_monto_haber_n3 = AsientoHaberDetalle.objects.filter(cuenta=n3)
                                    suma_monto_haber_n3 = 0
                                    for i in lista_monto_haber_n3:
                                        suma_monto_haber_n3 += i.monto
                                    saldo = suma_monto_debe_n3 - suma_monto_haber_n3
                                    if g.tipo_de_saldo == 'h':
                                        saldo *= -1 # por el tema del saldo, debe y haber, segun Luca Paccioli
                                    diccionario_balance[g][n1][n2][n3]['suma'] = saldo
                                    diccionario_balance[g][n1][n2]['suma'] += saldo
                            diccionario_balance[g][n1]['suma'] += diccionario_balance[g][n1][n2]['suma']
                    diccionario_balance[g]['suma'] += diccionario_balance[g][n1]['suma']
    # hasta aqui ya tenemos el balance

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
