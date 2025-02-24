from urllib import request
from django import forms
from django.core.exceptions import ValidationError
from produto.models import *
from .models import Caixa

class CaixaForm(forms.ModelForm):
    data = forms.DateTimeField(
        label="Data",
       
    )

    descricao = forms.CharField(
        label='Descrição',
        max_length=200,
        widget=forms.TextInput(
            attrs={'type': 'text', 'class': 'form-control', 'placeholder': 'Pagamento ou entrada Referente a ...'}
        )
    )
    valor = forms.CharField(
        label='Valor',
        max_length=14,
        widget=forms.TextInput(
            attrs={'type': 'text','data-mask':'###.###.##0,00' ,'data-mask-reverse':'true','size':'14','class':'form-control mask-money','placeholder':'Digite apenas numeros','defalt':'0,00'},
        
        )
    )
    tipo = forms.CharField(
        label= 'Operação',
        widget= forms.Select(
            attrs={'type':'select','class':'form-control'},
            choices={
                ('e','Entrada'),
                ('s','Saida'),
            },
        )
    )


    class Meta:
        model = Caixa
        fields = "__all__"

