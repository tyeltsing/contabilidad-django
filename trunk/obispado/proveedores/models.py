from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=40)
    ruc = models.CharField(max_length=11)
    #ver si quieren telefono e email
    
