from django.conf.urls.defaults import *
from aportantes.models import *
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings


reporter_lookup = {
	'queryset': Aportante.objects.all(),
	'field': 'nombre', # this is the field which is searched
	#'limit': 10, # default is to limit query to 10 results. Increase this if you like.
	#'login_required': False, # default is to allow anonymous queries. Set to True if you want authenticated access.
}

urlpatterns = patterns('',
    # Example:
    # (r'^obispado/', include('foo.urls')),

    (r'^$', 'obispado.views.index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^ingresos/', 'ingresos.views.index'),
    #(r'^carga/(?P<ap>\d+)/(?P<fe>\d+)/(?P<ruc>\d+)/(?P<cant>\d+)/(?P<des>\d+)/(?P<pu>\d+)/(?P<ex>\d+)/(?P<tot>\d+)$', 'ingresos.views.carga'),
    #(r'^carga_ingresos/', 'ingresos.views.carga_ingresos'),
    (r'^carga_ingresos/', 'obispado.ingresos.views.carga'),
    (r'^carga_egresos/', 'obispado.egresos.views.carga'),
    (r'^balances/$',  'obispado.balances.views.index'),
    (r'^balances/csv', 'obispado.balances.views.some_view'),
    (r'^solicitar_planilla_egresos/', 'obispado.egresos.views.solicitar_planilla_egresos'),
    (r'^generar_planilla_csv_egresos/', 'obispado.egresos.views.generar_planilla_csv_egresos'),
    #(r'^reporter_lookup/$', 'ingresos.views.json_lookup', reporter_lookup),
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),

)

