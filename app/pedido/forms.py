from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render
from .models import *

class Mesa_Form(forms.ModelForm):

    nome=forms.CharField(
        label='Mesa'
    )
    def clean_nome(self):
        data =Pedido.objects.filter(loja=User.loja, nome=self.cleaned_data["nome"] , status="aberto_c", tipo="Mesa")
        if data.exist():
            raise forms.ValidationError('Mesa ja esta aberta, corriga por favor.')
        
        return data
    
    
    class Meta():
        model = Pedido
        fields = ['nome',]
    
