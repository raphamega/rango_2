from django import forms
from.models import Pag_Contato


class ContactForm(forms.Form):
    nome_completo = forms.CharField(
    error_messages={'required': 'Obrigatório o preenchimento do nome'},
        widget=forms.TextInput(
            attrs={
                    "class": "form-control",
                    "placeholder": "Seu nome completo"
                }
            )
        )
    email= forms.EmailField(
        error_messages={'invalid': 'Digite um email válido!'},
        widget=forms.EmailInput(
            attrs={
                    "class": "form-control",
                    "placeholder": "Digite seu email"
                }
            )
        )
    mensagem= forms.CharField(
        error_messages={'required': 'É obrigatório o preenchimento do campo mensagem!'},
        widget=forms.Textarea(
            attrs={
                    "class": "form-control",
                    "placeholder": "Digite sua mensagem"
                }
            )
)
    class Meta:
        model = Pag_Contato
        fields = "__all__"