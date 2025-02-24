from django.shortcuts import get_object_or_404, render, redirect
from PIL import Image
import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView,ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib import messages
from loja.models import Loja_Model
from .models import *
from .forms import Produto_Form

# Create your views here.
@login_required
def produto_list(request):
    template_name = "produto/produto_list.html"
    produto = Produto_Model.objects.filter(loja=request.user.loja.id)
    if produto.exists():
        for obj in produto:
            if obj.estoque == 0 and obj.controle_estoque == True:
                obj.ativo = False
                obj.save()

    context=dict(
        object_list=produto
    )
    return render(request, template_name, context)

@login_required
def adicionar_Produto(request):
    template_name = 'produto/produto_form.html'
    form =  Produto_Form(request.POST or None)
    produto = Produto_Model.objects.filter(loja=request.user.loja, categoria='m')
    form.fields.get('imgrediente').queryset=produto
    context={
        'form':form,
        'titulo': "Cadastrar Produto",
        'botao': "Salvar",
    }
    if request.method == "POST":
        form =  Produto_Form(request.POST or None, request.FILES, )
        if form.is_valid():
            print('É valido')
            prod = form.save(commit=False)
            prod.loja=request.user.loja
            prod.save()

            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produto:produto_detail', pk=prod.pk)
           
        else:
            print('Não é valido')
            messages.error(request, 'Erro ao cadastrar produto.')
            context={
                'form':form,
                'titulo': "Configurar Usuario",
                'botao': "Salvar",
            }
    return render(request, template_name, context)

@login_required
def editar_produto(request, pk):
    template_name = 'produto/produto_form.html'
    produto = get_object_or_404(Produto_Model, pk=pk)
    form =  Produto_Form(request.POST or None, instance=produto)
    prod = Produto_Model.objects.filter(loja=request.user.loja, categoria='m')
    form.fields.get('imgrediente').queryset=prod
    context={
        'form':form,
        'object':produto,
        'titulo': "Cadastrar Produto",
        'botao': "Salvar",
    }
    if request.method == "POST":
        form =  Produto_Form(request.POST or None, request.FILES, instance=produto )
        if form.is_valid():
            print('É valido')
            form.save()
           

            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('produto:produto_detail', pk=pk)
           
        else:
            print('Não é valido')
            messages.error(request, 'Erro ao cadastrar produto.')
            context={
                'form':form,
                'titulo': "Cadastrar Produto",
                'botao': "Salvar",
            }
    return render(request, template_name, context)


class Produto_Detalhe(DetailView):
    template_name = 'produto/produto_detail.html'
    model=Produto_Model

class Produto_Edit(UpdateView): 
    template_name = 'produto/produto_form.html'
    model = Produto_Model
    form_class=Produto_Form
    success_url = reverse_lazy('produto:produto_list')
    success_message = "contact successfully created!"    

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)

        context['titulo'] =  "Editar Produto"
        context['botao'] = "Salvar"
        
        return context

class Produto_Delete(DeleteView): 
    template_name = 'produto/produto_delet.html'
    model = Produto_Model
    # form_class = Produto_Form
    success_url = reverse_lazy('produto:produto_list')
    success_message = "contact successfully created!"    

    def get_context_data(self,*args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['titulo'] =  "Deletar Produto"
        context['botao'] = "Confirme o Exclução Deste Item. Aqui"

        return context
