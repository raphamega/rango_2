from decimal import Decimal
from django.shortcuts import redirect, render
from pedido.models import Pedido, Item, Acrescimo, Mesa
from produto.models import Produto_Model
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .tests import *
from loja.models import Loja_Model


# Create your views here.
@login_required
def caixa_home(request):
    template_name = "caixa/caixa_home.html"
    form = CaixaForm()
    loja = Loja_Model.objects.get(usuario=request.user.id)
    print(loja)
    lista = Caixa.objects.all().filter(loja=request.user.loja.id).order_by("-data")
    notificacao = Pedido.objects.filter(loja=request.user.loja.id, status="enviado")
    entrada = Caixa.objects.filter(loja= request.user.loja.id, tipo="e")
    saida = Caixa.objects.filter(loja=request.user.loja.id, tipo="s")
    entTotal = 0
    for e in entrada:
        entTotal += Decimal(e.valor)

    saiTotal = 0
    for s in saida:
        saiTotal += Decimal(s.valor)

    saldo = entTotal-saiTotal


    context = dict(
        form=form,
        lista=lista,
        notificacao=notificacao,
        ent=entTotal,
        sai=saiTotal,
        saldo=saldo,
    )
    return render(request, template_name, context)

@login_required
def caixa_add(request):
    template = 'caixa:caixa_home'
    loja = Loja_Model.objects.get(usuario=request.user.id)
    notificacao = Pedido.objects.filter(loja=loja.id, status="enviado")
    form = CaixaForm()

    if request.method == "POST":
        form = CaixaForm(request.POST)
        tipo = request.POST.get('tipo')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')

        valor = valor.replace(".", "").replace(",", ".")
        caixa = Caixa.objects.create(
            loja=loja,
            tipo=tipo,
            descricao=descricao,
            valor=valor,
        )
        caixa.save()

    return redirect(template)

@login_required
def registradora_home(request, pk):
    template = "caixa/pdv.html"
    loja = Loja_Model.objects.get(usuario=request.user.id)
    produto = Produto_Model.objects.all().filter(loja=loja.id, ativo=True)
    bebida = Produto_Model.objects.filter(loja=loja.id, categoria='b', ativo=True)
    produto_adicionar = Produto_Model.objects.filter(loja=loja.id, categoria='a', ativo=True)
    notificacao = Pedido.objects.filter(loja=loja.id, status="enviado")
    mesa =Mesa.objects.filter(loja=loja.id, status="aberto_c")
    print(pk)
    if pk == 1:
        pedido = Pedido.objects.filter(loja=loja.id, venda="", status="aberto_c")
        if pedido.exists():
            pedido = Pedido.objects.filter(loja=loja.id, venda="", status="aberto_c").latest('pk').pk
            return redirect("caixa:registradora_home", pk=pedido)
        else:
            print('não, adcionar item ao pedido')
            pedido= Pedido.objects.create(
                loja=loja,
                usuario=request.user,
                status="aberto_c",
                venda = "",
                total_pedido=0.00,
                dinheiro = 0.00,
                pix =0.00,
                debito = 0.00,
                credito = 0.00,
            )
            pedido.save()
            pedido=Pedido.objects.get(id=pedido.id,)
            pedido.n_pedido=pedido.id
            pedido.save()

            item = Item.objects.filter(pedido=pedido.id)
            item_obj = Item.objects.filter(pedido = pedido.id).order_by('-id')

            total = 0
            for item in item:
                total+=Decimal(item.preco)


            context=dict(
                loja=loja,
                produto = produto,
                bebida = bebida,
                adcional = produto_adicionar,
                pedido=pedido,
                item=item_obj,
                acre_list=produto_adicionar,
                total = total,
                recebido= 0,
                faltante= 0 ,
                notificacao=notificacao,
                mesa=mesa,
            )
            return render(request, template, context)


    else:  
        pedido = Pedido.objects.get(pk=pk)
        item_obj = Item.objects.filter(pedido=pedido.id)
        lista = ""
        total = 0
        for item in item_obj:
            if item.item_acrescimo != "" and item.observacao != "":
                lista += f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
                total += item.preco

            if item.item_acrescimo == "" and item.observacao == "":
                lista += f"<strong>{item.qt} X {item.produto}</strong><br/><p>"
                total += item.preco

            if item.item_acrescimo != "" and item.observacao == "":
                lista += f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}"
                total += item.preco
                total += item.preco

            if item.item_acrescimo == "" and item.observacao != "":
                lista += f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"

        lista = lista
        pedido.total_pedido = total
        pedido.save()

        valor = Decimal(pedido.dinheiro)+Decimal(pedido.pix)+Decimal(pedido.debito)+Decimal(pedido.credito)

        item = Item.objects.filter(pedido=pedido.id)
        item_obj = Item.objects.filter(pedido=pedido.id).order_by('-id')

        total = 0
        for item in item:
            total += Decimal(item.preco)

        faltante = Decimal(valor)-Decimal(total)

        context = dict(
            loja=loja,
            produto=produto,
            bebida=bebida,
            adcional=produto_adicionar,
            pedido=pedido,
            item=item_obj,
            acre_list=produto_adicionar,
            total=total,
            recebido=valor,
            faltante=faltante,
            notificacao=notificacao,
            mesa=mesa,
        )
        
        return render(request, template, context)

@login_required
def busca_produto(request, pk):
    qbusca= request.GET.get('q')
    if qbusca :
        produto = Produto_Model.objects.filter(loja=request.user.loja, ativo=True, nome__icontains=qbusca)
        template="caixa/pdv.html"
        loja=Loja_Model.objects.get(usuario=request.user.id)
        bebida = Produto_Model.objects.filter(loja=loja.id, categoria='b', ativo=True)
        produto_adicionar = Produto_Model.objects.filter(loja=loja.id, categoria='a', ativo=True)
        notificacao = Pedido.objects.filter(loja=loja.id, status="enviado")
        mesa =Mesa.objects.filter(loja=loja.id, status="aberto_c")
        pedido = Pedido.objects.get(pk=pk,loja=loja.id)
        item_obj = Item.objects.filter(pedido=pedido.id)
        lista = ""
        total=0
        for item in item_obj:
            if item.item_acrescimo != "" and item.observacao !="" :
                lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
                total+=item.preco

            if item.item_acrescimo == "" and item.observacao =="" :
                lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>"
                total+=item.preco

            if item.item_acrescimo != "" and item.observacao =="" :
                lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}"
                total+=item.preco

            if item.item_acrescimo == "" and item.observacao !="" :
                lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
                total+=item.preco


        pedido.pedido = lista
        pedido.total_pedido=total
        pedido.save()


        valor = Decimal(pedido.dinheiro) + Decimal(pedido.pix) + Decimal(pedido.debito) + Decimal(pedido.credito)

        item = Item.objects.filter(pedido=pedido.id)
        item_obj = Item.objects.filter(pedido = pedido.id).order_by('-id')

        total = 0
        for item in item:
            total+=Decimal(item.preco)

        faltante = Decimal(valor)-Decimal(total)

        context=dict(
            loja=loja,
            produto = produto,
            bebida = bebida,
            adcional = produto_adicionar,
            pedido=pedido,
            item=item_obj,
            acre_list=produto_adicionar,
            total = total,
            recebido=valor,
            faltante=faltante,
            notificacao=notificacao,
            mesa=mesa,
        )
        return render(request, template, context)
    
    else:
        return redirect("caixa:registradora_home", pk=pk)

@login_required
def registradora_item(request, pk):
    pedido = request.POST.get('pedido_id')
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
            item_prod = Item.objects.filter(produto_id=pk, pedido=pedido.id, item_acrescimo="", observacao="")
            if item_prod.exists():
                print('2 - sim')
                item_prod = Item.objects.get(produto_id=pk, pedido=pedido.id, item_acrescimo="", observacao="")
                item_prod.qt += 1
                item_prod.preco += item_prod.produto.preco
                item_prod.save()
                print("salvo")

                if product_obj.controle_estoque == False :
                    produto = Produto_Model.objects.get(id=product_obj.id,loja=request.user.loja)
                    print("*****")
                    if produto.imgrediente == "" :
                        print('Sem Ingrediente')
                        if  produto.estoque == 1:
                            produto.estoque -= 1
                            produto.ativo = False
                            produto.save()
                        else:
                            produto.estoque -= 1
                            produto.save()

                    else:
                        for p in produto.imgrediente.all():
                            print(p.nome)
                            if  p.estoque == 1:
                                p.estoque -= 1
                                p.ativo = False
                                p.save()
                            else:
                                p.estoque -= 1
                                p.save()
                        print("*****")

                else: 
                    if product_obj.estoque == 1:
                        product_obj.estoque -= 1
                        product_obj.ativo = False
                        product_obj.save()
                    else:
                        product_obj.estoque -= 1
                        product_obj.save()

            else:
                print('1 -não')
                item = Item.objects.create(
                    pedido=pedido,
                    produto=product_obj,
                    qt=1,
                    preco=product_obj.preco,
                    observacao="",
                    item_acrescimo="",
                )
                item.save()
                print("salvo")
                if product_obj.controle_estoque == False :
                    produto = Produto_Model.objects.get(id=product_obj.id,loja=request.user.loja)
                    print("*****")
                    if produto.imgrediente == "" :
                        print('Sem Ingrediente')
                        if  produto.estoque == 1:
                            produto.estoque -= 1
                            produto.ativo = False
                            produto.save()
                        else:
                            produto.estoque -= 1
                            produto.save()

                    else:
                        for p in produto.imgrediente.all():
                            print(p.nome)
                            if  p.estoque == 1:
                                p.estoque -= 1
                                p.ativo = False
                                p.save()
                            else:
                                p.estoque -= 1
                                p.save()
                        print("*****")

                else: 
                    if product_obj.estoque == 1:
                        product_obj.estoque -= 1
                        product_obj.ativo = False
                        product_obj.save()
                    else:
                        product_obj.estoque -= 1
                        product_obj.save()

        else:
            item = Item.objects.create(
                pedido=pedido,
                produto=product_obj,
                qt=1,
                preco=product_obj.preco,
                observacao="",
                item_acrescimo="",
            )
            item.save()
            print("salvo")
            if product_obj.controle_estoque == False :
                produto = Produto_Model.objects.get(id=product_obj.id,loja=request.user.loja)
                print("*****")
                if produto.imgrediente == "" :
                    print('Sem Ingrediente')
                    if  produto.estoque == 1:
                        produto.estoque -= 1
                        produto.ativo = False
                        produto.save()
                    else:
                        produto.estoque -= 1
                        produto.save()

                else:
                    for p in produto.imgrediente.all():
                        print(p.nome)
                        if  p.estoque == 1:
                            p.estoque -= 1
                            p.ativo = False
                            p.save()
                        else:
                            p.estoque -= 1
                            p.save()
                    print("*****")

            else: 
                if product_obj.estoque == 1:
                    product_obj.estoque -= 1
                    product_obj.ativo = False
                    product_obj.save()
                else:
                    product_obj.estoque -= 1
                    product_obj.save()


    return redirect("caixa:registradora_home", pk=pedido.pk)

@login_required
def observacao(request):
    pedido = request.POST.get('pedido_id')
    id = request.POST.get("item_id")
    obs = request.POST.get("item_obs")
    qt = request.POST.get("item_qt")
    print(f"id: {id}  obs: {obs} Qt:{qt}")

    item = Item.objects.get(id=id)
    item.observacao = obs
    item.save()
    print("salvo")
    pedido =  Pedido.objects.get(id=pedido)
    return redirect("caixa:registradora_home", pk=pedido.pk)

@login_required
def registradora_remover_item(request):
    pedido = request.POST.get('pedido_id')
    id = request.POST.get('remove')
    print("***")
    print(f"id numero{id}")
    print("***")
    item = Item.objects.get(id=id)
    if item.item_acrescimo == "":
        print("sim")
        produto = Produto_Model.objects.get(id=item.produto.id, loja=request.user.loja)
        print(f"produto: {produto}")
        produto.estoque += item.qt
        produto.save()
        item.delete()


    else:
        print("não")
        produto = Produto_Model.objects.filter(id=item.produto.id, loja=request.user.loja)
        acre = Acrescimo.objects.filter(item=item.id)
        
        print(f"produto: {produto}, acres:{acre}")

        for p in produto:
            pro = Produto_Model.objects.get(id=p.id)
            if pro.controle_estoque == False and pro.imgrediente !="":
                print(f"{pro.nome}")
                for p2 in pro.imgrediente.all():
                    print(f"p: {p2} item.qt{item.qt}")
                    p2.estoque += item.qt
                    p2.save()
            else:
                produto = Produto_Model.objects.get(id=item.produto.id, loja=request.user.loja)
                print(f"produto: {produto}")
                produto.estoque += item.qt
                produto.save()

        for a in acre:
            print(f"{a.produto.nome} qt:{a.qt}")
            pro = Produto_Model.objects.get(id=a.produto.id)
            if pro.controle_estoque == False and pro.imgrediente !="":
                print(f"{pro.nome}")
                for p2 in pro.imgrediente.all():
                    print(f"p: {p2} item.qt{item.qt}")
                    p2.estoque += a.qt
                    p2.save()    

            else:
                produto = Produto_Model.objects.get(id=pro.id, loja=request.user.loja)
                print(f"produto: {produto}")
                produto.estoque += a.qt
                produto.save()  

        item.delete()
    pedido = Pedido.objects.get(id=pedido)
    return redirect("caixa:registradora_home", pk=pedido.pk)

@login_required
def registradora_acrecimo(request):
    loja_id = request.POST.get('loja_id')
    id = request.POST.get('add_id')
    pedido = request.POST.get('pedido_id')
    produto = request.POST.get('produto_id')
    item_id = request.POST.get('item_id')

    print(f' loja: {loja_id}\n produto: {produto}\n item: {item_id}\n add_id: {id}')

    pedido = Pedido.objects.get(id=pedido)
    produto = Produto_Model.objects.get(id=produto)
    item = Item.objects.get(id=item_id)
    acrescimo = Acrescimo.objects.filter(item=item.id, produto=produto.id)

    if acrescimo.exists():
        if produto.estoque>=item.qt:

            print(f' if >= Produto:{produto.estoque} item:{item.qt}')
            acrescimo = Acrescimo.objects.get(item=item.id, produto=produto.id)
            itemf = Item.objects.get(id=item.id)
            if itemf.qt == 1:
                acrescimo.qt += 1
                acrescimo.preco += Decimal(produto.preco)
                acrescimo.save()

                itemf.item_acrescimo = ""
                print(f'preco:{itemf.preco} produto{produto.preco}')
                itemf.preco += Decimal(produto.preco)
                itemf.save()
                acresf = Acrescimo.objects.filter(item=itemf.id)
                for acresf in acresf:
                    itemf.item_acrescimo += f'{acrescimo.produto}-{acresf.qt}<br>'
                    itemf.save()

                produto.estoque -= itemf.qt
                produto.save()
            else:
                print("mais q 1")
                print(f'antes{acrescimo.qt}')
                acrescimo.qt += 1
                print(f'depois{acrescimo.qt}')
                acrescimo.preco += Decimal(produto.preco) * itemf.qt
                acrescimo.save()
                acres = Acrescimo.objects.filter(item=item_id)
                itemf.item_acrescimo = ""
                print(f'preco:{itemf.preco} produto{itemf.produto.preco}')
                itemf.preco = itemf.produto.preco * itemf.qt
                print(f'preco:{itemf.preco} acrescimo{acrescimo.preco}')
                for i in acres:
                    i = Acrescimo.objects.get(id=i.id)
                    itemf.preco += i.preco
                    itemf.save()
                acresf = Acrescimo.objects.filter(item=item_id)
                for acresf in acresf:
                    itemf.item_acrescimo += f'{acrescimo.produto_nome}-{acresf.qt}<br>'
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
                    acrescimo.preco += Decimal(produto.preco)
                    acrescimo.save()

                    itemf.item_acrescimo = ""
                    print(f'preco:{itemf.preco} produto{produto.preco}')
                    itemf.preco += Decimal(produto.preco)
                    itemf.save()
                    acresf = Acrescimo.objects.filter(item=itemf.id)
                    for acresf in acresf:
                        itemf.item_acrescimo += f'{acrescimo.produto_nome}-{acresf.qt}<br>'
                        itemf.save()

                    produto.estoque -= itemf.qt
                    produto.save()
                else:
                    print("mais q 1")
                    print(f'antes{acrescimo.qt}')
                    acrescimo.qt += 1
                    print(f'depois{acrescimo.qt}')
                    acrescimo.preco += Decimal(produto.preco) * itemf.qt
                    acrescimo.save()
                    acres = Acrescimo.objects.filter(item=item_id)
                    itemf.item_acrescimo = ""
                    print(f'preco:{itemf.preco} produto{itemf.produto.preco}')
                    itemf.preco = itemf.produto.preco * itemf.qt
                    print(f'preco:{itemf.preco} acrescimo{acrescimo.preco}')
                    for i in acres:
                        i = Acrescimo.objects.get(id=i.id)
                        itemf.preco += i.preco
                        itemf.save()
                    acresf = Acrescimo.objects.filter(item=item_id)
                    for acresf in acresf:
                        itemf.item_acrescimo += f'{acrescimo.produto_nome}-{acresf.qt}<br>'
                        itemf.save()

                    produto.estoque -= itemf.qt
                    produto.ativo = False
                    produto.save()

            else:
                print(f' if  Produto:{produto.estoque} item:{item.qt}')
    else:
        print('Não o item_acrescimo não exist')
        if produto.estoque>=item.qt:
            print(f' if >= Produto:{produto.estoque} item:{item.qt}')
            acres = Acrescimo.objects.create(
                item=item,
                produto=produto,
                preco=Decimal(produto.preco),
                qt=1,
            )
            acres.save()

            item.item_acrescimo += f'{acres.produto}-{acres.qt}<br>'
            item.preco += acres.preco * item.qt
            item.save()

            acres.qt = 1
            acres.preco = acres.preco * item.qt
            acres.save()

            produto.estoque -= item.qt
            produto.save()
        else:
            if produto.estoque == item.qt:
                print(f' if == Produto:{produto.estoque} item:{item.qt}')
                acres = Acrescimo.objects.create(
                    item=item,
                    produto=produto.id,
                    produto_nome=produto.nome,
                    preco=produto.preco,
                    qt=1,
                )
                acres.save()

                item.item_acrescimo += f'{acres.produto_nome}-{acres.qt}<br>'
                item.preco += acres.preco * item.qt
                item.save()

                acres.qt = 1
                acres.preco = acres.preco * item.qt
                acres.save()

                produto.estoque -= item.qt
                produto.save()

            else:
                print(f' if  Produto:{produto.estoque} item:{item.qt}')

    if produto.estoque<=0:
        produto.ativo = False
        produto.save()

    return redirect("caixa:registradora_home", pk=pedido.pk)

@login_required
def acrescimo_list(request, pk):
    acrescimo = Acrescimo.objects.filter(item=pk)
    context = dict(
        acresc=acrescimo
    )
    return render(request, "pedido/acrescimo.html", context)

@login_required
def registradora_entrega(request, pk):
    pedido = Pedido.objects.get(pk=pk)
    item_obj = Item.objects.filter(pedido=pedido.id)
    lista = ""
    total=0
    for item in item_obj:
        if item.item_acrescimo != "" and item.observacao !="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
            total+=item.preco

        if item.item_acrescimo == "" and item.observacao =="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>"
            total+=item.preco

        if item.item_acrescimo != "" and item.observacao =="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}"
            total+=item.preco

        if item.item_acrescimo == "" and item.observacao !="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
            total+=item.preco


    print(f'{lista},{total}')
    if total<=0:
        pass
    else:
        if request.method == "POST":
            nome = request.POST.get('nome')
            telefone = request.POST.get('telefone')
            cep = request.POST.get('cep')
            endereco = request.POST.get('endereco')
            numero = request.POST.get('numero')
            complemento = request.POST.get('complemento')
            bairro = request.POST.get('bairro')
            municipio = request.POST.get('cidade')
            uf = request.POST.get('UF')
            dinheiro = request.POST.get("dinheiro")
            cartao = request.POST.get("cartao")
            troco = request.POST.get("troco")

            print(cep)

            if dinheiro is not None:
                PG = f"{dinheiro} {troco}"
            else:
                PG = "Cartão"

            pedido.n_pedido = pedido.id
            pedido.pedido = lista
            pedido.total_pedido = total
            pedido.nome = nome
            pedido.telefone = telefone
            pedido.cep = cep
            pedido.endereco = endereco
            pedido.numero = numero
            pedido.complemento = complemento
            pedido.bairro = bairro
            pedido.municipio = municipio
            pedido.uf = uf
            pedido.frm_pg = PG
            pedido.venda="Entrega"
            pedido.save()

            # return redirect('produto:ler_pedido', pk=pedido.id)

    return redirect('caixa:registradora_home', pk=pk)

@login_required
def registradora_pagamento(request, pk):
    pedido = Pedido.objects.get(id=pk, usuario=request.user.id)
    if request.method == "POST":
        dinheiro = request.POST.get("dinheiro")
        pix = request.POST.get("pix")
        debito = request.POST.get("debito")
        credito = request.POST.get("credito")

        if dinheiro == "":
            dinheiro = "0,00"

        if pix == "":
            pix = "0,00"

        if debito == "":
            debito = "0,00"

        if credito == "":
            credito = "0,00"

        print(f'dinheiro :{dinheiro}\npix :{pix}\ndebito :{debito}\ncredito:{credito}')
        dinheiro = dinheiro.replace(".", "").replace(",", ".")
        pix = pix.replace(".", "").replace(",", ".")
        debito = debito.replace(".", "").replace(",", ".")
        credito = credito.replace(".", "").replace(",", ".")

        pedido.dinheiro = dinheiro
        pedido.pix = pix
        pedido.debito = debito
        pedido.credito = credito
        pedido.save()

    valor = Decimal(pedido.dinheiro)+Decimal(pedido.pix)+Decimal(pedido.debito)+Decimal(pedido.credito)

    total = Decimal(valor)-Decimal(pedido.total_pedido)
    print(total)
    if pedido.total_pedido == valor:
        print(f'iguais pedido: {pedido.total_pedido} valor: {valor}')

    if pedido.total_pedido>=valor:
        print(f'iguais pedido: {pedido.total_pedido} valor: {valor}')

    return redirect("caixa:registradora_home", pk=pedido.pk)

@login_required
def registradora_pedido(request, pk):
    pedido = Pedido.objects.get(pk=pk)
    item_obj = Item.objects.filter(pedido=pedido.id)
    lista = ""
    total = 0
    for item in item_obj:
        lista += f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
        total += item.preco

    print(f'{lista},{total}')
    if total<=0:
        pass
    else:
        if request.method == "POST":
            nome = request.POST.get('nome')
            telefone = request.get('telefone')
            cep = request.POST.get('CEP')
            endereco = request.POST.get('endereco')
            numero = request.POST.get('numero')
            complemento = request.POST.get('complemento')
            bairro = request.POST.get('bairro')
            municipio = request.POST.get('cidade')
            uf = request.POST.get('estado')

            pedido.n_pedido = pedido.id
            pedido.pedido = lista
            pedido.total_pedido = total
            pedido.nome = nome
            pedido.telefone = telefone
            pedido.cep = cep
            pedido.endereco = endereco
            pedido.numero = numero
            pedido.complemento = complemento
            pedido.bairro = bairro
            pedido.municipio = municipio
            pedido.uf = uf
            pedido.status = "recebido"
            pedido.save()

            # return redirect('produto:ler_pedido', pk=pedido.id)

    return redirect('caixa:registradora_home', pk=pedido.pk)

@login_required
def registradora_aceitar_pedido(request, pk):
    pedido = Pedido.objects.get(id=pk, usuario=request.user.id)
    pedido.status = 'recebido'
    pedido.save()

    itens = Item.objects.filter(pedido=pedido.id)
    for itens in itens.all():
        pro = Produto_Model.objects.get(id=itens.produto.id)
        item = Item.objects.get(id=itens.id)
        pro.estoque -= item.qt
        pro.save()

    return redirect('pedido:mesa_list')

@login_required
def registradora_retirar_balcao(request, pk):
    pedido = Pedido.objects.get(pk=pk, usuario=request.user.id)


    item_obj = Item.objects.filter(pedido=pedido.id)
    lista = ""
    total=0
    for item in item_obj:
        if item.item_acrescimo != "" and item.observacao !="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
            total+=item.preco

        if item.item_acrescimo == "" and item.observacao =="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>"
            total+=item.preco

        if item.item_acrescimo != "" and item.observacao =="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}"
            total+=item.preco

        if item.item_acrescimo == "" and item.observacao !="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
            total+=item.preco

    
    if request.method == "POST":
        pedido.venda = "Balcão"
        pedido.pedido=lista
        pedido.total_pedido=total
        pedido.save()
        if pedido.total_pedido < 0:
            pedido.status= "recebido"
            pedido.save()

    return redirect('pedido:mesa_list')

@login_required
def registradora_retirar_mesa(request, pk):
    pedido = Pedido.objects.get(pk=pk, usuario=request.user.id)
    mesa= Mesa.objects.get(id=request.POST.get('mesa'))

    item_obj = Item.objects.filter(pedido=pedido.id)
    lista = ""
    total=0
    for item in item_obj:
        if item.item_acrescimo != "" and item.observacao !="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
            total+=item.preco

        if item.item_acrescimo == "" and item.observacao =="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>"
            total+=item.preco

        if item.item_acrescimo != "" and item.observacao =="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Acresc:</strong><br/>&nbsp;&nbsp;{item.item_acrescimo}"
            total+=item.preco

        if item.item_acrescimo == "" and item.observacao !="" :
            lista +=f"<strong>{item.qt} X {item.produto}</strong><br/><p>&nbsp;<strong>Observ:</strong><br/>&nbsp;&nbsp;{item.observacao}</p>"
            total+=item.preco



    if request.method == "POST":
        pedido.mesa=mesa
        pedido.nome=mesa.numero
        pedido.status='recebido'
        pedido.venda='Mesa'
        pedido.pedido=lista
        pedido.total_pedido=total
        pedido.save()

        mesa.total+=total
        mesa.save()

    return redirect('pedido:mesa_list')

@login_required
def fechar_mesa(request, pk):
    template_name= "caixa/fechar-mesa.html"
    mesa = Mesa.objects.get(pk=pk)
    pedido = Pedido.objects.filter(mesa=mesa.id)

    valor = Decimal(mesa.dinheiro)+Decimal(mesa.pix)+Decimal(mesa.debito)+Decimal(mesa.credito)
    
    total = 0
    for p in pedido:
        total += Decimal(p.total_pedido )

    faltante = Decimal(valor)-Decimal(total)

    context = dict(
        pedido=pedido,
        total=total,
        faltante=faltante,
        mesa=mesa,
        recebido=valor,
    )

    return render(request, template_name, context)

@login_required
def registradora_pagamento_mesa(request, pk):
    mesa = Mesa.objects.get(id=pk, loja=request.user.loja)
    # pedido = Pedido.objects.get(id=pk, usuario=request.user.id)
    if request.method == "POST":
        dinheiro = request.POST.get("dinheiro")
        pix = request.POST.get("pix")
        debito = request.POST.get("debito")
        credito = request.POST.get("credito")

        if dinheiro == "":
            dinheiro = "0,00"

        if pix == "":
            pix = "0,00"

        if debito == "":
            debito = "0,00"

        if credito == "":
            credito = "0,00"

        print(f'dinheiro :{dinheiro}\npix :{pix}\ndebito :{debito}\ncredito:{credito}')
        dinheiro = dinheiro.replace(".", "").replace(",", ".")
        pix = pix.replace(".", "").replace(",", ".")
        debito = debito.replace(".", "").replace(",", ".")
        credito = credito.replace(".", "").replace(",", ".")

        mesa.dinheiro = dinheiro
        mesa.pix = pix
        mesa.debito = debito
        mesa.credito = credito
        mesa.save()

    valor = Decimal(mesa.dinheiro)+Decimal(mesa.pix)+Decimal(mesa.debito)+Decimal(mesa.credito)

    total = Decimal(valor)-Decimal(mesa.total)
    print(total)

    
    if mesa.total == valor:
        print(f'iguais pedido: {mesa.total} valor: {valor}')

    if mesa.total>=valor:
        print(f'iguais pedido: {mesa.total} valor: {valor}')

    return redirect("caixa:fechar_mesa", pk=pk)

@login_required
def registradora_mesa_receber(request, pk):
    mesa = Mesa.objects.get(id=pk, loja=request.user.loja)
    if mesa.status == "Pago":
        return redirect('caixa:caixa_home')
    else:
        pedido = Pedido.objects.filter(mesa=mesa.id)
        lista = ""
        for item in pedido :
            lista += item.pedido

        
        caixa = Caixa.objects.create(
            loja=request.user.loja,
            tipo = "e",
            descricao = lista,
            valor =mesa.total,
        )
        caixa.save()

        mesa.status="Pago"
        mesa.save()

        return redirect('pedido:mesa_list')
