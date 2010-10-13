from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^obispado/', include('obispado.foo.urls')),

    (r'^$', 'obispado.views.index'),
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^ingresos/', 'obispado.ingresos.views.index'),
    #(r'^carga/(?P<ap>\d+)/(?P<fe>\d+)/(?P<ruc>\d+)/(?P<cant>\d+)/(?P<des>\d+)/(?P<pu>\d+)/(?P<ex>\d+)/(?P<tot>\d+)$', 'obispado.ingresos.views.carga'),
    #(r'^carga_ingresos/', 'obispado.ingresos.views.carga_ingresos'),
    (r'^carga_ingresos/', 'obispado.ingresos.views.carga'),
    (r'^carga_egresos/', 'obispado.egresos.views.carga'),
    (r'^balances/',  'obispado.balances.views.index'),
)
