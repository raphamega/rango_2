
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import *



class Produto_Form(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imgrediente'].required = False
        

    codigo = forms.CharField(
        label='Código do Produto',
        max_length=30,
        error_messages={"unique":"Código ja Cadastrado"},
        widget=forms.TextInput(
            attrs={'type': 'text','class': 'form-control', 'placeholder':'Digite um código para seu produto'}
        )
    )
    data_compra = forms.CharField(
        label='Data Compra ou Fabricação:',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control',
                   'placeholder': 'Data da Nota'},

        )
    )
    data_validade = forms.CharField(
        label='Data de Validade:',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control',
                   'placeholder': 'Data da Nota'},

        )
    )
    nome = forms.CharField(
        label='Nome do Produto',
        max_length=300,
        error_messages={"unique":"Produto ja Cadastrado"},
        widget=forms.TextInput(
            attrs={'type': 'text','class': 'form-control', 'placeholder':'Nome do produto'}
        
        )
    )
    categoria = forms.CharField(
        label= 'Categoria',
        widget=forms.Select(
            choices={
                ('f', 'Produto-Final'),
                ('m', 'Materia-Prima'),
                ('a', 'Acrescimo'),
                ('b', 'Bebida'),
            },
        )
    )
    descricao = forms.CharField(
        label='Descrição',
        max_length= 100,
        widget=forms.Textarea(
            attrs={'type': 'text','class': 'form-control', 'placeholder':'Descreva o produto', 'value':'Sem descrição'},
        )
    )
    preco_compra = forms.CharField(
        label='Valor de Compra',
        max_length=14,
        widget=forms.TextInput(
            attrs={'type': 'decimal/text','data-mask':'##0.00' ,'data-mask-reverse':'true', 'class':'form-control mask-money','placeholder':'Digite apenas numeros'},
        
        )
    )
    preco = forms.CharField(
        label='Valor de Venda',
        max_length=14,
        widget=forms.TextInput(
            attrs={'type': 'decimal/text','data-mask':'##0.00' ,'data-mask-reverse':'true', 'class':'form-control mask-money','placeholder':'Digite apenas numeros'},
        
        )
    )
    estoque = forms.CharField(
        label='Quantidade Total ',
        max_length=30,
        widget=forms.TextInput(
            attrs={'type': 'number','class': 'form-control', 'placeholder':'Total'}
        
        )
    )
    estoque_minimo = forms.CharField(
        label='Quantidade Minima',
        max_length=30,
        widget=forms.TextInput(
            attrs={'type': 'number','class': 'form-control', 'placeholder':'Total'}
        
        )
    )
    image = forms.FileField()

    imgrediente = forms.ModelMultipleChoiceField(
        label='Ingredientes',
        queryset=Produto_Model.objects.filter(categoria='m', controle_estoque=True, ativo=True),
        widget=forms.CheckboxSelectMultiple,
    )
    
    
    class Meta:
        model = Produto_Model
        fields = [
            'image',
            'codigo',
            'data_compra',
            'data_validade',
            'nome',
            'categoria',
            'descricao',
            'preco_compra',
            'preco',
            'estoque',
            'estoque_minimo',
            'controle_estoque',
            'ativo',
            'imgrediente',

        ]

