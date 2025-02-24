from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from produto.models import Produto_Model
from loja.models import Loja_Model

# Create your models here.
    
class Und_Medida(models.Model):
    nome = models.CharField(max_length=30, null=True, blank=True)
    
    def __str__(self):
        return self.nome
    

class Fornecedor_Model(models.Model):
    loja = models.ForeignKey(Loja_Model, related_name='fornecedor', on_delete=models.CASCADE)
    nome = models.CharField(max_length=30, null=True)
    cnpj = models.CharField(max_length=200, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True)
    cep = models.CharField(max_length=30, null=True)
    endereco = models.CharField(max_length=300, null=True)
    numero = models.CharField(max_length=10, null=True)
    complemento = models.CharField(max_length=100, null=True)
    bairro = models.CharField(max_length=300, null=True)
    municipio = models.CharField(max_length=300, null=True)
    UF = models.CharField(max_length=30, null=True)
    objects = models.Manager()

    def __str__(self):
        return self.nome
    


MOVIMENTO = (
    ('e', 'entrada'),
    ('s', 'saida'),
)

class Nota_Model(models.Model):
    loja = models.ForeignKey(Loja_Model, related_name='nota', on_delete=models.CASCADE)
    #fornecedor =models.ForeignKey(Fornecedor_Model, on_delete=models.CASCADE)
    nf = models.CharField('Nota Fiscal', max_length=10, null=True, blank=True)
    dia = models.CharField(max_length=10, null=True, blank=True)
    movimento = models.CharField(choices=MOVIMENTO, max_length=1)
    total = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=10, null=True,blank=True, default='aberto')
    objects = models.Manager()

    def __str__(self):
        return self.nf

    def get_absolute_url(self):
        return reverse_lazy('estoque:estoque_detail', kwargs={'pk': self.pk})

    

class Item_Model(models.Model):
    loja = models.ForeignKey(Loja_Model, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto_Model, on_delete=models.CASCADE)
    nota = models.ForeignKey(Nota_Model, related_name='item',on_delete=models.CASCADE)
    data_validade = models.CharField(max_length=30, null=True)
    ncm = models.CharField(max_length=50, null=True, blank=True)
    unidade = models.ForeignKey(Und_Medida, on_delete=models.PROTECT,null=True, blank=True)
    quantidade = models.IntegerField( null=True, blank=True)
    preco_unid = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    preco = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        #return f'{self.pk} {self.nota} {self.produto}'
        return f'{self.pk}'
    
    
