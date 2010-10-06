from django.db import models

TIPO_SALDO_CHOICES = (
                     ('d', 'Debe'),
                     ('h', 'Haber')
)

class TipoCuenta(models.Model):
    '''Activo, Pasivo, Patrimonio_Neto, Perdidas, Ganancias, etc...'''
    # hace falta esta clase? porque se puede hacer una lista como los *CHOICES
    nombre = models.CharField(max_length=40)
    tipo_de_saldo = models.CharField(max_length=1, choices=TIPO_SALDO_CHOICES)
    # monto = ?
    def __unicode__(self):
        return self.nombre


class CuentaNivel1(models.Model):
    '''he?'''
    nombre = models.CharField(max_length=40)
    tipo = models.ForeignKey(TipoCuenta)
    def __unicode__(self):
        return self.nombre

class CuentaNivel2(models.Model):
    nombre = models.CharField(max_length=40)
    tipo = models.ForeignKey(CuentaNivel1)
    def __unicode__(self):
        return self.nombre

    
class CuentaNivel3(models.Model):
    nombre = models.CharField(max_length=40)
    tipo = models.ForeignKey(CuentaNivel2)
    def __unicode__(self):
        return self.nombre
    
