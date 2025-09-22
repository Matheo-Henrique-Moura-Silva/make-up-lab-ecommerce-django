import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET, require_POST
from django.contrib.messages import constants
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from adminSite.models import Categoria, Marca, Produto
from comprar.models import Item, Cliente, Carrinho, Favorito


def ver_produto(request, id):
    if request.user.is_authenticated and not request.user.is_superuser:
        produto_poo = Produto.objects.get(id=id)
        carrinho_poo = Carrinho.objects.get(usuario_id=request.user.id)
        favorito_poo = Favorito.objects.get(usuario_id=request.user.id)
        try:
            item_poo = Item.objects.get(produto_id=id)
        except:
            item_poo = None
        produto_status = False
        produto_favorito = False
        produto_quantidade = 1
        if carrinho_poo.produto_existe(produto_poo.id):
            produto_status = True
            produto_quantidade = carrinho_poo.get_qntd_item(produto_poo.id)
        if favorito_poo.produto_existe(produto_poo.id):
            produto_favorito = True
        return render(request, 'comprar/produto.html', {'produto': produto_poo, 'carrinho': carrinho_poo, 'favorito': favorito_poo, 'isFavorito': produto_favorito, 'isCarrinho': produto_status, 'quantidade': produto_quantidade, 'item': item_poo})
    else:
        produto_poo = Produto.objects.get(id=id)
        return render(request, 'comprar/produto.html', {'produto': produto_poo})

@require_GET
def adicionar_item_carrinho(request, id, qntd):
    try:
        quantidade = int(qntd)
        if quantidade <= 0:
            return HttpResponse(f"O valor {qntd} é invalido.")
    except ValueError:
        return HttpResponse(f"{qntd} - Não é um valor válido.")
    else:
        try:
            produto = get_object_or_404(Produto, id=id)
            carrinho = get_object_or_404(Carrinho, usuario_id=request.user.id)
        except:
            messages.error(request, "Você precisa estar logado no sistema para adicionar itens ao carrinho.")
            return JsonResponse({'status': 'error', 'message': 'O Você precisa ser maior ou igual a 1 para adicionar no carrinho!'})
        else:
            item = None
            for item_aux in carrinho.itens.all():
                if item_aux.produto.id == produto.id:
                    item = item_aux
                    break
            if item:
                item.set_quantidade(qntd)
                item.save()
                messages.success(request, f'"{item.produto.nome}" foi alterado a quantidade no carrinho!')
                return JsonResponse({'status': 'success', 'message': 'Item alterado no carrinho!'})
            else:
                item = Item.objects.create(produto=produto, quantidade=qntd)
                carrinho.adicionar_item(item.id)
                messages.success(request, f'"{item.produto.nome}" adicionado ao carrinho com sucesso!')
                return JsonResponse({'status': 'success', 'message': 'Item adicionado ao carrinho!'})

@login_required
def ver_carrinho(request):
    carrinho_poo = Carrinho.objects.get(usuario_id=request.user.id)
    itens_poo = carrinho_poo.itens.all()
    return render(request, 'comprar/ver_carrinho.html', {'itens': itens_poo, 'carrinho': carrinho_poo})

@login_required
def remover_item_carrinho(request, id):
    if request.method == "GET":
        return redirect('/comprar/ver_carrinho')
    elif request.method == "POST":
        item = Item.objects.get(id=id)
        item.delete()
        messages.add_message(request, constants.ERROR, f'Item "{item.produto.nome}" removido com sucesso.')
        return redirect('/comprar/ver_carrinho')

@require_GET
@login_required
def editar_item_carrinho(request, id, qntd):
    try:
        quantidade = int(qntd)
        if quantidade <= 0:
            return HttpResponse(f"O valor {qntd} é invalido.")
    except ValueError:
        return HttpResponse(f"{qntd} - Não é um valor válido.")
    else:
        try:
            item = get_object_or_404(Item, id=id)
            item.set_quantidade(qntd)
            item.save()
        except:
            messages.error(request, "Você precisa estar logado no sistema para editar itens do carrinho.")
            return JsonResponse({'status': 'error', 'message': 'Faça login para editar itens do carrinho!'})
        else:
            messages.success(request, f'"{item.produto.nome}" editado a quantidade para {qntd} unidades!')
        return JsonResponse({'status': 'success', 'message': 'Item do carrinho editado!'})

@login_required
def limpar_carrinho(request, id):
    try:
        carrinho = get_object_or_404(Carrinho, id=id)
    except:
        messages.error(request, f"Aconteceu um erro inesperado ao consultar o carrinho com esse ID={id}.")
        return redirect('/comprar/ver_carrinho')
    else:
        try:
            carrinho = get_object_or_404(Carrinho, id=id)
            carrinho_is_vazio = carrinho.get_total_itens()
            carrinho.limpar()
        except:
            messages.error(request, f"Aconteceu um erro inesperado ao tentar limpar o carrinho com esse ID={id}.")
            return redirect('/comprar/ver_carrinho')
        else:
            if carrinho_is_vazio == 0:
                messages.warning(request, "O Carrinho já está vazio.")
                return redirect('/comprar/ver_carrinho')
            else:
                messages.success(request, "Todos os itens do carrinho fora removidos com sucesso.")
                return redirect('/comprar/ver_carrinho')

@require_GET
@login_required
def adicionar_produto_favorito(request, id):
    try:
        produto_poo = get_object_or_404(Produto, id=id)
        favorito_poo = Favorito.objects.get(usuario_id=request.user.id)
    except:
        messages.error(request, "Você precisa estar logado no sistema para adicionar itens ao carrinho.")
        return JsonResponse({'status': 'error', 'message': 'Erro, faça login no sistema.'})
    else:
        if favorito_poo.produto_existe(produto_poo.id):
            if favorito_poo.del_favorito(produto_poo.id):
                messages.success(request, f'"{produto_poo.nome}" removido dos favoritos com sucesso!')
                return JsonResponse({'status': 'success', 'message': 'Item removido dos favoritos!'})
        else:
            if favorito_poo.add_favorito(produto_poo.id):
                messages.success(request, f'"{produto_poo.nome}" adicionado aos favoritos com sucesso!')
                return JsonResponse({'status': 'success', 'message': 'Item adicionado aos favoritos!'})
        messages.error(request, "Erro ao salvar produto dos favoritos.")
        return JsonResponse({'status': 'error', 'message': 'Erro ao salvar produto dos favoritos.'})

@login_required
def ver_favoritos(request):
    carrinho_poo = Carrinho.objects.get(usuario_id=request.user.id)
    favorito_poo = Favorito.objects.get(usuario_id=request.user.id)
    favorito_poo = favorito_poo.get_todos_favoritos()
    return render(request, 'comprar/ver_favoritos.html', {'carrinho': carrinho_poo, 'favoritos': favorito_poo})

def buscar_produto(request):
    if request.method == "GET":
        palavra_chave = request.GET.get("pesquisa").upper()
        produtos_poo = Produto.objects.all()
        produtos_pesquisa = list()
        if palavra_chave != '':
            for produto in produtos_poo:
                if palavra_chave in produto.nome.upper() or palavra_chave in produto.descricao:
                    produtos_pesquisa.append(produto)

        if request.method == "GET":
            marca_selecionada = request.GET.get('marca')
            categoria_selecionada = request.GET.get('categoria')

            produtos_filtrados = produtos_pesquisa

            marca_poo = None
            categoria_poo = None
            # Lógica de filtro: Se a marca for selecionada, filtra por ela
            if marca_selecionada:
                marca_selecionada = int(marca_selecionada)
                produtos_filtrados = [p for p in produtos_filtrados if p.marca.id == marca_selecionada]
                marca_poo = Marca.objects.get(id=marca_selecionada)

            # Lógica de filtro: Se a categoria for selecionada, filtra por ela
            if categoria_selecionada:
                categoria_selecionada = int(categoria_selecionada)
                produtos_filtrados = [p for p in produtos_filtrados if p.categoria.id == categoria_selecionada]
                categoria_poo = Categoria.objects.get(id=categoria_selecionada)

        produtos_pesquisa = produtos_filtrados

        paginator_produtos = Paginator(produtos_pesquisa, 16)
        # Obtenha o número da página da URL, ou use 1 como padrão
        page_number = request.GET.get('page')
        # Obtenha o objeto da página solicitada
        page_obj = paginator_produtos.get_page(page_number)
        try:
            carrinho_poo = Carrinho.objects.get(usuario_id=request.user.id)
            favorito_poo = Favorito.objects.get(usuario_id=request.user.id)
            produtos_status = list()
            produtos_favoritos = list()
            produtos_quantidade = list()
            for produto in page_obj:
                if carrinho_poo.produto_existe(produto.id):
                    produtos_quantidade.append(carrinho_poo.get_qntd_item(produto.id))
                    produtos_status.append(True)
                else:
                    produtos_quantidade.append(1)
                    produtos_status.append(False)
                if favorito_poo.produto_existe(produto.id):
                    produtos_favoritos.append(True)
                else:
                    produtos_favoritos.append(False)
            page_obj2 = page_obj
            page_obj = zip(page_obj, produtos_status, produtos_favoritos, produtos_quantidade)
            marcas = Marca.objects.all()
            categorias = Categoria.objects.all()
        except:
            marcas = Marca.objects.all()
            categorias = Categoria.objects.all()
            page_obj2 = page_obj
            page_obj = zip(page_obj, page_obj, page_obj, page_obj)
            return render(request, 'comprar/buscar_produto.html', {'produtos': page_obj, 'produtos2': page_obj2, 'pesquisa': palavra_chave, 'marca_poo': marca_poo, 'categoria_poo': categoria_poo, 'marcas': marcas, 'categorias': categorias})
        else:
            page_obj2 = page_obj
            return render(request, 'comprar/buscar_produto.html', {'produtos': page_obj, 'produtos2': page_obj2, 'carrinho': carrinho_poo, 'pesquisa': palavra_chave, 'marca_poo': marca_poo, 'categoria_poo': categoria_poo, 'marcas': marcas, 'categorias': categorias})
