from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from cpf_field.models import CPFField
from cnpj_field.models import CNPJField

# Create your models here.

class Usuario_Model(models.Model):
    usuario = models.OneToOneField(User, related_name='perfil', on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length=300, null=True)
    cpf = CPFField(max_length=18, unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)
    endereco = models.CharField(max_length=300, null=True, blank=True)
    numero = models.CharField(max_length=10,null=True, blank=True)
    bairro = models.CharField(max_length=300, null=True, blank=True)
    municipio = models.CharField(max_length=300, null=True, blank=True)
    UF = models.CharField(max_length=2, null=True, blank=True)
    objects = models.Manager()

    def __str__(self):
        return f"{self.nome_completo}"
    
CATEGORIA = (
    ('b', 'Bares'),
    ('l', 'Lanchonete'),
    ('r', 'Restaurante'),
)


class Loja_Model(models.Model):
    usuario = models.OneToOneField(User,related_name='loja', on_delete=models.CASCADE)
    loja = models.CharField(max_length=150, null=True)
    cnpj = CNPJField(max_length=18, unique=True, null=True, blank=True)#00.000.000/0000-00
    telefone = models.CharField(max_length=16, null=True)#(99) 9 9999-9999
    cep = models.CharField(max_length=10, null=True)#99.999-999
    endereco = models.CharField(max_length=150, null=True)
    numero = models.CharField(max_length=10, null=True)
    complemento = models.CharField(max_length=150, null=True)
    bairro = models.CharField(max_length=150, null=True)
    municipio = models.CharField(max_length=150, null=True)
    UF = models.CharField(max_length=2, null=True)
    image = models.FileField(upload_to='loja/', null=True, blank=True)
    ativo = models.BooleanField(default=True)
    aberto = models.BooleanField(default=False)
    categoria = models.CharField(choices=CATEGORIA, max_length=1)
    tipo = models.CharField(max_length=10, default='comercio')
    objects = models.Manager()

    def __str__(self):
        return str(self.loja)

    def get_absolut_url(self):
        return reverse_lazy("loja:loja_vitrine", kwargs={"pk": self.pk})