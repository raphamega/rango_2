from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.db.models import Q
from loja.models import Loja_Model

# Create your models h
class Produto_Model(models.Model):
    loja = models.ForeignKey(Loja_Model, on_delete=models.CASCADE)
    codigo= models.CharField(max_length=10, unique=True, null=True, blank=True)
    data_compra = models.CharField(max_length=10, null=True, blank=True)
    data_validade = models.CharField(max_length=10, null=True, blank=True)
    nome = models.CharField(max_length=300, unique=True, null=True, blank=True)
    categoria = models.CharField(max_length=20, null=True, blank=True)
    descricao = models.TextField(max_length=500, null=True, blank=True)
    preco_compra = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    preco = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    estoque=models.IntegerField( null=True, blank=True)
    estoque_minimo=models.IntegerField( null=True, blank=True)	
    controle_estoque = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    image = models.ImageField(upload_to='produto/',  blank=True, null=True)
    imgrediente=models.ManyToManyField('Produto_Model',related_name="ingre", blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.nome
    
       
    def get_absolute_url(self):
        return reverse_lazy('produto:produto_detail', kwargs={'pk':self.pk})
    
    