from urllib import request
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import *




class Fornecedor_Form(forms.ModelForm):
    nome = forms.CharField(
        label='Nome Fantasia',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'placeholder': 'Digite o nome fantasia da loja'}
        )
    )
    responsavel = forms.CharField(
        label='Razão Social',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'placeholder': 'Digite o nome fantasia da loja'}
        )
    )
    cnpj = forms.CharField(
        label='CNPJ',
        max_length=18,
        widget=forms.TextInput(
            attrs={'type': 'text', 'data-mask': '00.000.000/0000-00', 'class': 'form-control mask-cnpj',
                   'placeholder': 'Digite apenas Numeros', 'required': 'False'}
        )
    )
    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        widget=forms.TextInput(
            attrs={'type': 'text', 'data-mask': '000.000.000-00', 'class': 'form-control mask-cpf',
                   'placeholder': 'Digite apenas Numeros', 'required': 'False'}
        )
    )
    telefone = forms.CharField(
        label='Celular',
        max_length=16,
        widget=forms.TextInput(
            attrs={'type': 'text', 'data-mask': '(00) 0 0000-0000',
                   'class': 'form-control', 'placeholder': 'Digite apenas Numeros'}
        )
    )
    cep = forms.CharField(
        label='CEP',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_cep', 'data-mask': '00000-000',
                   'class': 'form-control', 'placeholder': '12345-000', }
        )
    )
    endereco = forms.CharField(
        label='Rua, Av, etc',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_endereco',
                   'class': 'form-control', 'placeholder': 'Endereco do Bar'}
        )
    )
    numero = forms.CharField(
        label='Numero',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'placeholder': 'Numero'}
        )
    )
    complemento = forms.CharField(
        label='Complemento',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'value': 'Sem Complemento'}
        )
    )
    bairro = forms.CharField(
        label='Bairro',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_bairro',
                   'class': 'form-control', 'placeholder': 'Bairro'}
        )
    )
    municipio = forms.CharField(
        label='Municipio',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_municipio',
                   'class': 'form-control', 'placeholder': 'Cidade'}
        )
    )
    UF = forms.CharField(
        label='UF',
        max_length=2,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_UF',
                   'class': 'form-control', 'placeholder': 'Estado'}
        )
    )

    class Meta:
        model = Fornecedor_Model
        fields = '__all__'

class Nota_Form(forms.ModelForm):
    
    dia = forms.CharField(
        label='Data Nota:',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control',
                   'placeholder': 'Data da Nota'},

        )
    )

    nf = forms.CharField(
        label='Nota Fiscal:',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control',
                   'placeholder': 'Numero da Nota'},

        )
    )
    movimento = forms.CharField(
        label='Movimento:',
        max_length=7,
        widget=forms.Select(
            attrs={'type': 'select', 'class': 'form-control'},
            choices={
                ('e', 'Entrada'),
                ('s', 'Saida'),
            },
        )
    )
    # total = forms.CharField(
    #     label='Valor Total da Nota ',
    #     max_length=14,
    #     widget=forms.TextInput(
    #         attrs={'type': 'decimal/text', 'data-mask': '#####0.00', 'data-mask-reverse': 'true',
    #                'class': 'form-control mask-money', 'placeholder': '0,00'},
    #     )
    # )

    class Meta:
        model = Nota_Model
        fields = [
            #'fornecedor',
            'nf',
            'dia',
            'movimento',
            # 'total',
        ]

class Item_Form(forms.ModelForm):
    
  
    quantidade = forms.CharField(
        label='QT:',
        max_length=7,
        widget=forms.TextInput(
            attrs={'type': 'number/text', 'class': 'form-control', 'data-mask': '####00',
                   'data-mask-reverse': 'true', 'class': 'form-control mask-money', 'onfocus':'calcular()', 'placeholder': 'Quantidade'},

        )
    )
    preco_unid = forms.CharField(
        label='Vl Unid',
        max_length=14,
        widget=forms.TextInput(
            attrs={'type': 'decimal/text', 'maxlength': '14', 'data-mask': '########0.00',
                   'data-mask-reverse': 'true', 'class': 'form-control mask-money', 'onblur':'calcular()', 'placeholder': '0,00'},
        )
    )
    preco = forms.CharField(
        label='Vl Total',
        widget=forms.TextInput(
            attrs={'type': 'decimal/text', 'data-mask': '########0.00', 'maxlength': '14',
                   'data-mask-reverse': 'true', 'class': 'form-control mask-money', 'placeholder': '0,00'},
        )
    )
    data_validade = forms.CharField(
        label='Data de Validade',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'date', 'class': 'form-control'},

        )
    )
    ncm = forms.CharField(
        label='NCM',
        max_length=8,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'maxlength': '8',
                   'data-mask': '######000', 'data-mask-reverse': 'true', 'placeholder': 'Quantidade'},

        )
    )
    
    class Meta:
        model = Item_Model
        fields = [
            'data_validade',
            'ncm',
            'unidade',
            'quantidade',
            'preco_unid',
            'preco',
        ]
    


