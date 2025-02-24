from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from produto.models import Produto_Model
from pedido.models import Pedido
from caixa.models import Caixa
from django.contrib import messages
from .models import *
from .forms import *

# Create your views here.
# INICIO VITRINE
@login_required
def pedido_item(request):
    pk= request.POST.get('produto_id')
    loja_id = request.POST.get('loja_id')
    pedido=request.POST.get('pedido_id')

    lojaslug=Loja_Model.objects.get(id=loja_id)
    pedido = Pedido.objects.get(id=pedido)
    if pk is not None:
        try:
            product_obj = Produto_Model.objects.get(id=pk)
        except Produto_Model.DoesNotExist:
            print("Mostrar mensagem ao usuário, esse produto acabou!")
            return redirect("cart:home")

        item_prod = Item.objects.filter(produto=pk)
        if item_prod.exists():
            print('1 - sim')
           
            item_prod=Item.objects.filter(produto_id=pk, pedido=pedido.id, item_acrescimo="", observacao="")
            if item_prod.exists():
                print('2 - sim')
                item_prod=Item.objects.get(produto_id=pk, pedido=pedido.id, item_acrescimo="", observacao="")
                item_prod.qt+=1
                item_prod.preco+=item_prod.produto.preco
                item_prod.save()
                print("salvo")
                if  product_obj.estoque == 1:    
                    product_obj.estoque -= 1
                    product_obj.ativo = False
                    product_obj.save()
                else:
                    product_obj.estoque -= 1
                    product_obj.save()

            else:
                print('1 -não')
                item = Item.objects.create(
                    pedido=pedido ,
                    produto= product_obj,
                    qt = 1,
                    preco = product_obj.preco,
                    observacao="",
                    item_acrescimo="",
                )
                item.save()
                print("salvo")
                if  product_obj.estoque == 1:    
                    product_obj.estoque -= 1
                    product_obj.ativo = False
                    product_obj.save()
                else:
                    product_obj.estoque -= 1
                    product_obj.save()

        else:
            item = Item.objects.create(
                pedido=pedido ,
                produto= product_obj,
                qt = 1,
                preco = product_obj.preco,
                observacao="",
                item_acrescimo="",
            )
            item.save()
            print("salvo")
            if  product_obj.estoque == 1:    
                product_obj.estoque -= 1
                product_obj.ativo = False
                product_obj.save()
            else:
                product_obj.estoque -= 1
                product_obj.save()
  
    return redirect("loja:loja_vitrine",slug=lojaslug.loja)

@login_required
def observacao(request):
    loja_id = request.POST.get('loja_id')
    lojaslug=Loja_Model.objects.get(id=loja_id)
    id = request.POST.get("item_id")
    obs = request.POST.get("item_obs")
    qt = request.POST.get("item_qt")
    print(f"id: {id}  obs: {obs} Qt:{qt}")

    item = Item.objects.get(id=id)
    item.observacao = obs
    item.save()
    print("salvo")
    
    return redirect("loja:loja_vitrine",slug=lojaslug.loja)

@login_required
def remover_item(request):
    loja_id = request.POST.get('loja_id')
    lojaslug=Loja_Model.objects.get(id=loja_id)
    id = request.POST.get('remove')
    print("***")
    print(f"id numero{id}")
    print("***")
    pedido = request.POST.get('pedido_id')
    print(pedido)
    acre = Acrescimo.objects.filter(item=id)
    item = Item.objects.get(id=id, pedido=pedido)

    for acre in acre.all():
        acre = Acrescimo.objects.get(id=acre.id)
        produto = Produto_Model.objects.get(id=int(acre.produto))
        produto.estoque += acre.qt * item.qt
        if produto.estoque >= 0 :
            produto.ativo = True    
        
        produto.save()
        acre.delete()

    
    produto = Produto_Model.objects.get(id=item.produto.id)
    produto.estoque+= item.qt
    produto.save()
    item.delete()

    return redirect("loja:loja_vitrine",slug=lojaslug.loja)

@login_required
def pedido_acrecimo(request):
    loja_id = request.POST.get('loja_id')
    id = request.POST.get('add_id')
    pedido= request.POST.get('pedido_id')
    produto = request.POST.get('produto_id')
    item_id = request.POST.get('item_id')
    
    print(f' loja: {loja_id}\n produto: {produto}\n item: {item_id}\n add_id: {id}')

    lojaslug = Loja_Model.objects.get(id=loja_id)
    pedido= Pedido.objects.get(id=pedido)
    produto = Produto_Model.objects.get(id=produto)
    item = Item.objects.get(id=item_id)
    acrescimo = Acrescimo.objects.filter(item=item.id, produto=produto.id)

    if acrescimo.exists():
        if produto.estoque >= item.qt :
 
            print(f' if >= Produto:{produto.estoque} item:{item.qt}')
            acrescimo = Acrescimo.objects.get(item=item.id, produto=produto.id)
            itemf = Item.objects.get(id=item.id)
            if itemf.qt == 1:
                acrescimo.qt += 1
                acrescimo.preco += produto.preco
                acrescimo.save()

                itemf.item_acrescimo=""
                print(f'preco:{itemf.preco} produto{produto.preco}')
                itemf.preco += produto.preco
                itemf.save()
                acresf =  Acrescimo.objects.filter(item = itemf.id)
                for acresf in acresf:
                    itemf.item_acrescimo += f'{acrescimo.produto_nome}-{acresf.qt}<br>'
                    itemf.save() 

                produto.estoque -= itemf.qt
                produto.save()
            else:
                print("mais q 1")
                print(f'antes{acrescimo.qt}')
                acrescimo.qt+= 1
                print(f'depois{acrescimo.qt}')
                acrescimo.preco+=produto.preco*itemf.qt
                acrescimo.save()
                acres =  Acrescimo.objects.filter(item = item_id)
                itemf.item_acrescimo=""
                print(f'preco:{itemf.preco} produto{itemf.produto.preco}')
                itemf.preco = itemf.produto.preco*itemf.qt
                print(f'preco:{itemf.preco} acrescimo{acrescimo.preco}')
                for i in acres:
                    i= Acrescimo.objects.get(id=i.id)
                    itemf.preco+=i.preco
                    itemf.save()
                acresf =  Acrescimo.objects.filter(item = item_id)
                for acresf in acresf:
                    itemf.item_acrescimo+=f'{acrescimo.produto_nome}-{acresf.qt}<br>'
                    itemf.save() 

                produto.estoque -= itemf.qt
                produto.save()    
        else:
            if produto.estoque == item.qt:
                print(f' if == Produto:{produto.estoque} item:{item.qt}')
                acrescimo = Acrescimo.objects.get(item=item.id, produto=produto.id)
                itemf = Item.objects.get(id=item.id)
                if itemf.qt == 1:
                    acrescimo.qt += 1
                    acrescimo.preco += produto.preco
                    acrescimo.save()

                    itemf.item_acrescimo=""
                    print(f'preco:{itemf.preco} produto{produto.preco}')
                    itemf.preco += produto.preco
                    itemf.save()
                    acresf =  Acrescimo.objects.filter(item = itemf.id)
                    for acresf in acresf:
                        itemf.item_acrescimo += f'{acrescimo.produto_nome}-{acresf.qt}<br>'
                        itemf.save() 

                    produto.estoque -= itemf.qt
                    produto.save()
                else:
                    print("mais q 1")
                    print(f'antes{acrescimo.qt}')
                    acrescimo.qt+= 1
                    print(f'depois{acrescimo.qt}')
                    acrescimo.preco+=produto.preco*itemf.qt
                    acrescimo.save()
                    acres =  Acrescimo.objects.filter(item = item_id)
                    itemf.item_acrescimo=""
                    print(f'preco:{itemf.preco} produto{itemf.produto.preco}')
                    itemf.preco = itemf.produto.preco*itemf.qt
                    print(f'preco:{itemf.preco} acrescimo{acrescimo.preco}')
                    for i in acres:
                        i= Acrescimo.objects.get(id=i.id)
                        itemf.preco+=i.preco
                        itemf.save()
                    acresf =  Acrescimo.objects.filter(item = item_id)
                    for acresf in acresf:
                        itemf.item_acrescimo+=f'{acrescimo.produto_nome}-{acresf.qt}<br>'
                        itemf.save() 

                    produto.estoque -= itemf.qt
                    produto.ativo = False
                    produto.save() 
                    
            else:
                print(f' if  Produto:{produto.estoque} item:{item.qt}')
    else:
        print('Não o item_acrescimo não exist')
        if produto.estoque >= item.qt :
            print(f' if >= Produto:{produto.estoque} item:{item.qt}')
            acres = Acrescimo.objects.create(
                item = item,
                produto= produto.id,
                produto_nome = produto.nome,
                preco = produto.preco,
                qt = 1,
            )
            acres.save()
            
            item.item_acrescimo+=f'{acres.produto_nome}-{acres.qt}<br>'
            item.preco+=acres.preco*item.qt
            item.save()

            acres.qt=1
            acres.preco=acres.preco*item.qt
            acres.save()

            produto.estoque -= item.qt
            produto.save()
        else:
            if produto.estoque == item.qt :
                print(f' if == Produto:{produto.estoque} item:{item.qt}')
                acres = Acrescimo.objects.create(
                    item = item,
                    produto= produto.id,
                    produto_nome = produto.nome,
                    preco = produto.preco,
                    qt = 1,
                )
                acres.save()
                
                item.item_acrescimo+=f'{acres.produto_nome}-{acres.qt}<br>'
                item.preco+=acres.preco*item.qt
                item.save()

                acres.qt=1
                acres.preco=acres.preco*item.qt
                acres.save()

                produto.estoque -= item.qt
                produto.save()

            else:
                print(f' if  Produto:{produto.estoque} item:{item.qt}')

    if produto.estoque <= 0 :
        produto.ativo = False    
        produto.save()

    return redirect("loja:loja_vitrine",slug=lojaslug.loja)

@login_required
def acrescimo_list(request,pk):
    acrescimo = Acrescimo.objects.filter(item=pk)
    context = dict(
        acresc = acrescimo
    )
    return render(request, "pedido/acrescimo.html", context)

#Fim VITRINE 

# INICIO CONTROLE DE MESAS
@login_required
def mesa_list(request):
    template_name = "caixa/list_mesa.html"
    loja = Loja_Model.objects.get(usuario=request.user)
    enviado = Pedido.objects.filter(loja=loja.id, status="enviado")
    recebido = Pedido.objects.filter(loja=loja.id, status="recebido")
    entrega = Pedido.objects.filter(loja=loja.id, status="entrega")
    finalizado = Pedido.objects.filter(loja=loja.id, status="finalizado")
    pedido = Pedido.objects.filter(loja=loja.id)

    mesa =Mesa.objects.filter(loja=loja.id, status="aberto_c")
    pedi =Pedido.objects.filter(loja=loja.id, status="aberto_c")
    context = dict(
        mesa=mesa,
        pedido=pedi,
        enviado=enviado,
        recebido=recebido,
        entrega=entrega,
        finalizado=finalizado,
        pp=pedido,
    )

    return render(request, template_name, context)

@login_required
def mesa_criar(request):
    if request.method == 'POST' :
        nome=request.POST.get("mesa")
        data =Mesa.objects.filter(loja=request.user.loja, numero=nome, status="aberto_c")
        if data.exists():
            loja = Loja_Model.objects.get(usuario=request.user)
            enviado = Pedido.objects.filter(loja=loja.id, status="enviado")
            recebido = Pedido.objects.filter(loja=loja.id, status="recebido")
            entrega = Pedido.objects.filter(loja=loja.id, status="entrega")
            finalizado = Pedido.objects.filter(loja=loja.id, status="finalizado")

            mesa =Mesa.objects.filter(loja=loja.id, status="aberto_c")
            pedi =Pedido.objects.filter(loja=loja.id, status="aberto_c")
            context=dict(
                mes="Mesa ja esta aberta, corriga por favor.",
                mesa=mesa,
                pedido=pedi,
                enviado=enviado,
                recebido=recebido,
                entrega=entrega,
                finalizado=finalizado,
            )
            return render(request,"caixa/list_mesa.html", context)
        else:
            print('É valido')
            mesa= Mesa.objects.create(
                loja = request.user.loja,
                numero=request.POST.get("mesa"),
                total= 0.00,
                dinheiro= 0.00,
                pix= 0.00,
                debito= 0.00,
                credito= 0.00,
                fiado= 0.00,
                frm_pg="",
                status= "aberto_c",
            )
            mesa.save()
            return redirect('pedido:mesa_list')

@login_required
def pedido_criar(request):
    pedido= Pedido.objects.create(
            loja=request.user.loja,
            usuario=request.user,
            status="aberto_c",
            total_pedido=0.00,
            dinheiro = 0.00,
            pix =0.00,
            debito = 0.00,
            credito = 0.00,
    )
    pedido.save()
    ped=Pedido.objects.get(id=pedido.id,)
    ped.n_pedido=pedido.id
    ped.save()

    return redirect("pedido:mesa_list")

@login_required
def pedido_delete(request, pk):
    ped =Pedido.objects.get(id=pk)
    ped.delete()
    print("Deletado")

    return redirect("pedido:mesa_list")

@login_required
def mesa_delete(request, pk):
    ped =Mesa.objects.get(id=pk)
    ped.delete()
    print("Deletado")

    return redirect("pedido:mesa_list")

@login_required
def ler_pedido(request, pk):
    ped =Pedido.objects.get(id=pk, loja=request.user.loja)

    context = dict(
        pedido=ped,
    )

    return render(request,"pedido/ler-pedido.html", context)

@login_required
def pedido_pronto(request, pk):
    ped =Pedido.objects.get(id=pk, loja=request.user.loja)
    print(ped.venda)
    if ped.venda == "Entrega":
        ped.status="entrega"
        ped.save()
    else:
        ped.status="finalizado"
        ped.save()
        caixa = Caixa.objects.create(
            loja=request.user.loja,
            tipo = "e",
            descricao = ped.pedido,
            valor =ped.total_pedido,
        )
        caixa.save()

    return redirect("pedido:mesa_list")

@login_required
def pedido_recebido(request, pk):
    ped =Pedido.objects.get(id=pk, loja=request.user.loja)
    ped.status="finalizado"
    ped.save()

    caixa = Caixa.objects.create(
        loja=request.user.loja,
        tipo = "e",
        descricao = ped.pedido,
        valor =ped.total_pedido,
    )
    caixa.save()

    return redirect("pedido:mesa_list")

# FIM CONTROLE MESA