import os
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from PIL import Image
from .forms import *
from .models import *


# Create your views here.
@login_required
def loja_home(request):
    template_name = "loja/loja_home.html"
    return render(request, template_name)    

@login_required
def gerarUsuario(request):
    template_name = 'registration/form-usuario-add.html'
    form = Usuario_Form(request.POST or None)
    context={
        'form':form,
        'titulo': "Registrar novo Usuario",
        'botao': "Salvar",
    }
    if request.method == "POST":
        if form.is_valid():
            print('É valido')
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            usuario = Usuario_Model.objects.create(
                usuario =user,
                nome_completo = f"{user.first_name} {user.last_name}",
            )
            usuario.save()

            img = Image.open(os.path.join(settings.BASE_DIR,f'static_local/img/semImage.png'))
            path =os.path.join(settings.BASE_DIR,f'static_rcm/media_root/loja/semImage.png')
            img = img.save(path)

            loja = Loja_Model.objects.create(
                usuario= user ,
                image='loja/semImage.png',
            )
            loja.save()

            usuario.save()
            
            messages.success(request, 'Usuario cadastrado com sucesso!')
            return redirect('login')
        else:
            print('Não é valido')
            messages.error(request, 'Erro ao cadastrar usuario.')
            context={
                'form':form,
                'titulo': "Registrar novo Usuario",
                'botao': "Salvar",
            }
            print(form.error_messages)
    return render(request, template_name, context)

@login_required
def gerarPerfil(request):
    template_name= 'registration/form-usuario-up.html'
    perfil = Usuario_Model.objects.get(usuario = request.user)
    form =  Perfil_Form(request.POST or None, instance=perfil)
    context={
        'form':form,
        'titulo': "Configurar Usuario",
        'botao': "Salvar",
    }
    if request.method == "POST":
        if form.is_valid():
            print('É valido')
            form.save()
            messages.success(request, 'Usuario cadastrado com sucesso!')
            return redirect('loja:loja_home')
        else:
            print('Não é valido')
            messages.error(request, 'Erro ao cadastrar usuario.')
            context={
                'form':form,
                'titulo': "Configurar Usuario",
                'botao': "Salvar",
            }
    return render(request, template_name, context)


class Loja_Update(UpdateView):
    model = Loja_Model
    template_name = "loja/loja_form.html"
    form_class = Loja_Form
    success_url = reverse_lazy('loja:loja_home')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Loja_Model, usuario=self.request.user)
        return self.object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Loja"
        context['botao'] = "Salvar"

        return context

# def gerarLoja(request):
#     template_name= 'loja/loja_form.html'
#     perfil = Loja_Model.objects.get(usuario = request.user)
#     form =  Loja_Form(request.POST or None, instance=perfil)
#     context={
#         'form':form,
#         'titulo': "Configurar Loja",
#         'botao': "Salvar",
#     }
#     if request.method == "POST":
        
#         if form.is_valid():
#             print('É valido')
#             form.save()
#             # image = request.FILES.get('image')

#             # loja = Loja_Model.objects.get(usuario=request.user)
#             # image = 'produto/'+image.name
#             # loja.save()

#             # img = Image.open(image)
#             # path = os.path.join(settings.BASE_DIR, f'static_rcm/media_root/produto/{image.name}')
#             # img = img.save(path)

#             messages.success(request, 'Loja cadastrado com sucesso!')
#             return redirect('loja:loja_home')
#         else:
#             print('Não é valido')
#             messages.error(request, 'Erro ao cadastrar usuario.')
#             context={
#                 'form':form,
#                 'titulo': "Configurar loja",
#                 'botao': "Salvar",
#             }
#     return render(request, template_name, context)