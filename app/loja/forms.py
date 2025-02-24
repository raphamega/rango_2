from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import *

# Usuario
class Usuario_Form(UserCreationForm):
    username = forms.CharField(
        label='E-mail',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'email', 'class': 'form-control', 'placeholder': 'seuemail@provedor.com'}
        )
    )
   
    first_name = forms.CharField(
        label='Primeiro Nome',
        max_length=100,
        widget=forms.TextInput(
            attrs={'type': 'text','class': 'form-control', 'placeholder':'Digite seu primeiro Nome'}
        )
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=300,
        widget=forms.TextInput(
            attrs={'type': 'text','class': 'form-control', 'placeholder':'Digite o restante do seu Nome'}
        )
    )
    password1 = forms.CharField(
        label='Senha',
        max_length=30,
        widget=forms.TextInput(
            attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Senha'}
        )
    )
    password2 = forms.CharField(
        label='Confirma Senha',
        max_length=30,
        widget=forms.TextInput(
            attrs={'type': 'password', 'class': 'form-control', 'placeholder': 'Confirmar Senha'}
        )
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2',
        ]
    # def clean_username(self):
    #     e = self.cleaned_data['username']
    #     if User.objects.filter(username=e).exists():
    #         raise ValidationError("Cadastro ja está em uso")

class Perfil_Form(forms.ModelForm):
    nome_completo = forms.CharField(
        label= 'Nome Completo',
        widget= forms.TextInput(
            attrs={'type':'text','class':'form-control'},
            
        )
    )
    cpf = forms.CharField(
        label='CPF',
        max_length=20,
        widget=forms.TextInput(
            attrs={'type': 'text','data-mask':'000.000.000-00' ,'class': 'form-control mask-cpf', 'placeholder': 'Digite apenas Numeros'}
        )

    )
    telefone = forms.CharField(
        label='Celular',
        max_length=30,
        widget=forms.TextInput(
            attrs={'type': 'text','data-mask':'(00) 0 0000-0000' , 'class': 'form-control', 'placeholder': 'Digite apenas Numeros'}
        )
    )
    cep = forms.CharField(
        label='CEP',
        max_length=9,
        widget=forms.TextInput(
            attrs={'type': 'text','id':'id_cep' ,'data-mask':'00000-000' , 'class': 'form-control', 'placeholder': '12345-000', }
        )
    )
    endereco = forms.CharField(
        label='Endereco',
        max_length=200,
        widget=forms.TextInput(
            attrs={'type': 'text','id':'id_endereco', 'class': 'form-control', 'placeholder': 'Endereco do Bar'}
        )
    )
    numero= forms.CharField(
        label='Numero',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Numero'}
        )
    )
    complemento = forms.CharField(
        label='Complemento',
        max_length=200,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'value': 'Sem Complemento'}
        )
    )
    bairro = forms.CharField(
        label='Bairro',
        max_length=100,
        widget=forms.TextInput(
            attrs={'type': 'text','id':'id_bairro', 'class': 'form-control', 'placeholder': 'Bairro'}
        )
    )
    municipio = forms.CharField(
        label='Municipio',
        max_length=200,
        widget=forms.TextInput(
            attrs={'type': 'text','id':'id_municipio', 'class': 'form-control', 'placeholder': 'Cidade'}
        )
    )
    UF = forms.CharField(
        label='UF',
        max_length=2,
        widget=forms.TextInput(
            attrs={'type': 'text','id':'id_UF','class': 'form-control', 'placeholder': 'Estado'}
        )
    )

    class Meta:
        model = Usuario_Model
        fields = [
            'nome_completo',
            'cpf',
            'telefone',
            'cep',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'municipio',
            'UF',
        ]        


# Loja
CATEGORIA = (
    ('b', 'Bares'),
    ('l', 'Lanchonete'),
    ('r', 'Restaurante'),


)

class Loja_Form(forms.ModelForm):

    loja = forms.CharField(
        label='Nome da Loja',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Digite o nome fantasia da loja'}

        )
    )
    categoria = forms.CharField(
        label='Categoria',
        widget=forms.Select(
            attrs={'type': 'select', 'class': 'form-control'},
            choices={
                ('b', 'Bares'),
                ('l', 'Lanchonete'),
                ('r', 'Restaurante'),
            },
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
    telefone = forms.CharField(
        label='Celular',
        max_length=16,
        widget=forms.TextInput(
            attrs={'type': 'text', 'data-mask': '(00) 0 0000-0000', 'class': 'form-control',
                   'placeholder': 'Digite apenas Numeros'}
        )
    )
    cep = forms.CharField(
        label='CEP',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_cep', 'data-mask': '00000-000', 'class': 'form-control',
                   'placeholder': '12345-000'}
        )
    )
    endereco = forms.CharField(
        label='Rua, Av, etc',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_endereco', 'class': 'form-control', 'placeholder': 'Endereco do Bar'}
        )
    )
    numero = forms.CharField(
        label='Numero',
        max_length=10,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Numero'}
        )
    )
    complemento = forms.CharField(
        label='Complemento',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'value': 'Sem Complemento'}
        )
    )
    bairro = forms.CharField(
        label='Bairro',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_bairro', 'class': 'form-control', 'placeholder': 'Bairro'}
        )
    )
    municipio = forms.CharField(
        label='Municipio',
        max_length=150,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_municipio', 'class': 'form-control', 'placeholder': 'Cidade'}
        )
    )
    UF = forms.CharField(
        label='UF',
        max_length=2,
        widget=forms.TextInput(
            attrs={'type': 'text', 'id': 'id_UF', 'class': 'form-control', 'placeholder': 'Estado'}
        )
    )
    image = forms.FileField()
   
    class Meta:
        model = Loja_Model
        fields = [
            'loja',
            'categoria',
            'cnpj',
            'telefone',
            'cep',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'municipio',
            'UF',
            'image',
        ]

        
