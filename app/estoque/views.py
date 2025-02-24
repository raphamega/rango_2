from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib import messages
from caixa.models import Caixa
from produto.models import Produto_Model
from .models import Nota_Model
from .forms import *

def estoque_lista(request):
    template_name = "estoque/estoque_list.html"
    object = Nota_Model.objects.filter(loja=request.user.loja, status="fechada")
    context=dict(
        object_list=object
    )
    return render(request, template_name, context)

class Estoque_Detalhe(DetailView):
    template_name = 'estoque/estoque_detail.html'
    model = Nota_Model
    context_object_name = 'nota'

def estoque_movimento(request):
    template_name = "estoque/estoque_form.html"
    nota = Nota_Model.objects.filter(status="aberto", loja=request.user.loja)
    if nota.exists():
        nota = Nota_Model.objects.get(status="aberto", loja=request.user.loja)
       
        return redirect('estoque:estoque_add', pk = nota.id)
    else:
        return redirect('estoque:nota_abrir')
       
    return render(request, template_name, context)

def nota_abrir(request):
    template_name = "estoque/estoque_form.html"
    form1 =  Nota_Form(request.POST or None)
    context={
        'form1':form1,
        'titulo': "Gerar Nota",
        'botao': "Gerar",
    }
    if request.method == "POST":
        form1 =  Nota_Form(request.POST or None)
        if form1.is_valid():
            print('É valido')
            prod = form1.save(commit=False)
            prod.loja=request.user.loja
            prod.save()
           
            messages.success(request, 'Nota Foi cadastrado com sucesso!')
            return redirect('estoque:estoque_move')
        else:
            print('Não é valido')
            messages.error(request, 'Erro ao cadastrar produto.')
        
        context={
            'form1':form1,
            'titulo': "Configurar Usuario",
            'botao': "Salvar",
        }
        
    return render(request, template_name, context)

def adcionar_item(request,pk):
    template_name = "estoque/estoque_form.html"  
    nota = Nota_Model.objects.get(id = pk)
    item = Item_Model.objects.filter(nota=nota, loja=request.user.loja)
    produto = Produto_Model.objects.filter(loja=request.user.loja)
    form = Item_Form(request.POST or None)
    context=dict(
        form=form,
        nota=nota,
        item=item,
        produto = produto,
    )
    if request.method == "POST":
        form =  Item_Form(request.POST or None)
        if form.is_valid():
            print('É valido')
            produto = Produto_Model.objects.get(id=request.POST.get('prod'))
            f = form.save(commit=False)
            f.produto= produto
            f.nota = nota
            f.loja = request.user.loja
            f.save()
                
            messages.success(request, 'Item adcionado com sucesso!')
            return redirect('estoque:estoque_move')
        

        else:
            
            print('Não é valido')
            messages.error(request, 'Erro ao cadastrar produto.')
            context=dict(
                form=form,
                nota=nota,
            )
       
    return render(request, template_name, context)

def gerar_nota(request):

    nf_id = request.POST.get('nota_id')
    nota = Nota_Model.objects.get(id=nf_id)
    item = Item_Model.objects.filter(nota=nota.id)

    vl=0
    for n in item:
        vl+= Decimal(n.preco)

    nota.total = vl
    nota.status = "fechada"
    nota.save()
    print(nota.id)

    if nota.movimento == "e":
        for i in item:
            produto=Produto_Model.objects.get(nome = i.produto)
            produto.estoque += Decimal(i.quantidade)
            produto.data_validade = i.data_validade
            produto.preco_compra = Decimal(i.preco_unid)
            if produto.preco == 0.00:
                vl = Decimal(i.preco_unid)
                produto.preco = vl*(vl*Decimal(99/100)+vl)
            produto.ativo = True
            produto.save()

            caixa = Caixa.objects.create(
                loja=request.user.loja,
                tipo= "s",
                descricao=f"Nota compra n°:{nota.nf}",
                valor=nota.total,
            )
            caixa.save()

    else:
        for i in item:
            produto=Produto_Model.objects.get(nome = i.produto)
            produto.estoque -= Decimal(i.quantidade)
            if produto.estoque <= 0:
                produto.ativo = False
            produto.save()  

            caixa = Caixa.objects.create(
                loja=request.user.loja,
                tipo= "e",
                descricao=f"Nota venda n°:{nota.nf}",
                valor=nota.total,
            )
            caixa.save()


    return redirect("estoque:estoque_list")

def excluir_nota(request):
    nf_id = request.POST.get('delete_id')
    nota = Nota_Model.objects.get(id=nf_id, loja=request.user.loja)
    nota.delete()

    print(f" excluido {nota.id}")

    return redirect("estoque:estoque_list")    

def excluir_item(request):
    nf_id = request.POST.get('item_id')
    item = Item_Model.objects.get(id=nf_id, loja=request.user.loja)
    item.delete()

    return redirect("estoque:estoque_move")   
