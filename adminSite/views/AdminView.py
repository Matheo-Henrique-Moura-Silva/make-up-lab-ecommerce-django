from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants
from django.http import HttpResponse
from django.shortcuts import render, redirect
from adminSite.models import Categoria, Marca, Produto


def admin_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard/')
    elif request.method == 'GET':
        return render(request, 'admin/entrar.html')
    else:
        email = request.POST.get('username_email')
        senha = request.POST.get('password')
        usuario = authenticate(email=email, password=senha)
        if usuario is not None and usuario.is_superuser == 1:
            login(request, usuario)
            return redirect('dashboard/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos.')
            return render(request, 'admin/entrar.html')

@login_required
def dashboard_view(request):
    if request.user.is_authenticated and request.user.is_superuser == 1:
        return render(request, 'admin/home.html')

@login_required
def produtos_view(request):
    if request.user.is_authenticated and request.user.is_superuser == 1:
        if request.method == "GET":
            categorias_poo = Categoria.objects.all()
            marcas_poo = Marca.objects.all()
            produtos_poo = Produto.objects.all()
            return render(request, 'admin/produtos.html', {'categorias': categorias_poo, 'marcas': marcas_poo, 'produtos': produtos_poo})
        elif request.method == "POST":
            nome = request.POST.get('nome')
            descricao = request.POST.get('descricao')
            preco = float(request.POST.get('preco'))
            custo = float(request.POST.get('custo'))
            estoque = request.POST.get('estoque')
            if estoque == '':
                estoque = 0
            imagem = request.FILES.get('imagem')
            categoria = request.POST.get('categoria')
            marca = request.POST.get('marca')

            produto = Produto(nome=nome,
                              descricao=descricao,
                              preco=preco,
                              custo=custo,
                              estoque=estoque,
                              imagem_capa=imagem,
                              categoria_id=categoria,
                              marca_id=marca)

            produto.save()
            categorias_poo = Categoria.objects.all()
            marcas_poo = Marca.objects.all()
            produtos_poo = Produto.objects.all()
            messages.add_message(request, constants.SUCCESS, 'Novo produto cadastrado')
            return render(request, 'admin/produtos.html', {'categorias': categorias_poo, 'marcas': marcas_poo, 'produtos': produtos_poo})

@login_required()
def excluir_produto_view(request, id):
    if request.method == "GET":
        return redirect('/adminsite/produtos')
    elif request.method == "POST":
        produto = Produto.objects.get(id=id)
        produto.delete()
        messages.add_message(request, constants.ERROR, 'Produto removido com sucesso.')
        return redirect('/adminsite/produtos')

@login_required()
def editar_produto_view(request, id):
    if request.method == "GET":
        return redirect('/adminsite/produtos')
    elif request.method == "POST":
        produto = Produto.objects.get(id=id)
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        preco = request.POST.get('preco')
        custo = request.POST.get('custo')
        estoque = request.POST.get('estoque')
        imagem = request.FILES.get('imagem')
        categoria = request.POST.get('categoria')
        marca = request.POST.get('marca')
        produto.nome = nome
        produto.descricao = descricao
        if preco != '':
            produto.preco = float(preco)
        if custo != '':
            produto.custo = float(custo)
        produto.estoque = estoque
        if imagem != None:
            produto.imagem_capa = imagem
        produto.categoria_id = categoria
        produto.marca_id = marca
        produto.save()
        messages.add_message(request, constants.WARNING, 'Produto editado com sucesso.')
        return redirect('/adminsite/produtos')

def sair_admin_view(request):
    logout(request)
    return render(request, 'admin/entrar.html')
