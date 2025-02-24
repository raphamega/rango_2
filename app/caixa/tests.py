from django.test import TestCase
from django.shortcuts import redirect, render
from pedido.models import Pedido, Item, Acrescimo, Mesa
from produto.models import Produto_Model

# Create your tests here.
def registradora_remover_item(request):
    pedido = request.POST.get('pedido_id')
    id = request.POST.get('remove')
    print("***")
    print(f"id numero{id}")
    print("***")
    item = Item.objects.get(id=id)
    if item.acrescimo.exists():
        print("sim")
    else:
        print("não")
    return   