from django.db import models
from loja.models import Loja_Model

# Create your models here.
class Caixa(models.Model):
    loja = models.ForeignKey(Loja_Model, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True)
    descricao =  models.CharField(max_length=300, null=True, blank=True)
    valor = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    dinheiro = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    pix = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    debito = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    credito = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    fiado = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    tipo = models.CharField(max_length=7, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return str(self.pk)
    
    
