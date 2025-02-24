from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from loja.models import *
# from cliente.models import *
from produto.models import *

# Create your models here.
class Mesa(models.Model):
    loja = models.ForeignKey(Loja_Model, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10,null=True, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    dinheiro = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    pix = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    debito = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    credito = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    fiado = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    frm_pg = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True, default='aberto')
    objects = models.Manager()


    def __str__(self):
        return str(f' Pedido: {self.pk} Mesa: {self.numero}')
    
    def get_mesa_url(self):
       return reverse_lazy("caixa:fechar_mesa", kwargs={"pk":self.pk})



class Pedido(models.Model):
    dia = models.DateField(auto_now_add=True)
    loja = models.ForeignKey(Loja_Model, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, related_name='ped_mesa',null=True, blank=True, on_delete=models.CASCADE)
    venda = models.CharField(max_length=10, null=True, blank=True)
    pedido = models.TextField(null=True, blank=True)
    total_pedido = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    nome = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    cep = models.CharField(max_length=30, null=True, blank=True)
    endereco = models.CharField(max_length=300, null=True, blank=True)
    numero = models.CharField(max_length=10, null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=300, null=True, blank=True)
    municipio = models.CharField(max_length=300, null=True, blank=True)
    uf = models.CharField(max_length=30, null=True, blank=True)
    dinheiro = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    pix = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    debito = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    credito = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    fiado = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    frm_pg = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=10, null=True, blank=True, default='aberto')

    objects = models.Manager()

    def __str__(self):
        return str(f' Pedido: {self.pk} Nome = {self.nome}')


    def get_pedido_url(self):
       return reverse_lazy("caixa:registradora_home", kwargs={"pk":self.pk})
    
    def get_ler_url(self):
       return reverse_lazy("pedido:ler_pedido", kwargs={"pk":self.pk})



class Item(models.Model):
    pedido = models.ForeignKey(Pedido,related_name='item_ped', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto_Model, related_name='item_prod', on_delete=models.CASCADE)
    qt = models.DecimalField(decimal_places=0, max_digits=4, null=True, blank=True)
    preco = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)
    item_acrescimo = models.TextField(null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.pk)


class Acrescimo(models.Model):
    item = models.ForeignKey(Item, related_name='arecimo', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto_Model, related_name='produto', on_delete=models.CASCADE)
    qt = models.DecimalField(decimal_places=0, max_digits=4, null=True, blank=True)
    preco = models.DecimalField(decimal_places=2, max_digits=14, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.pk)



