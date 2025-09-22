from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import constants
from adminSite.models import Produto, Marca, Categoria
from contas.models import Usuario, Cliente
from comprar.models import Carrinho, Favorito
from django.core.paginator import Paginator


def home_view(request):
    if request.user.is_superuser:
        logout(request)
        return redirect('login/')
    else:
        produtos_poo = Produto.objects.all()
        if request.method == "GET":
            marca_selecionada = request.GET.get('marca')
            categoria_selecionada = request.GET.get('categoria')

            produtos_filtrados = produtos_poo

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

        produtos_poo = produtos_filtrados

        paginator_produtos = Paginator(produtos_poo, 16)
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
            return render(request, 'home/home.html', {'produtos': page_obj, 'produtos2': page_obj2, 'marcas': marcas, 'categorias': categorias, 'marca_poo': marca_poo, 'categoria_poo': categoria_poo}, status=200)
        else:
            return render(request, 'home/home.html', {'produtos': page_obj, 'carrinho': carrinho_poo, 'produtos2': page_obj2, 'marcas': marcas, 'categorias': categorias, 'marca_poo': marca_poo, 'categoria_poo': categoria_poo}, status=200)

def logar_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'GET':
        return render(request, 'home/logar.html')
    else:
        email = request.POST.get('username_email')
        senha = request.POST.get('password')
        usuario = authenticate(email=email, password=senha)
        if usuario is not None and not usuario.is_superuser:
            login(request, usuario)
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos.')
            return render(request, 'home/logar.html')

def cadastrar_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    elif request.method == 'GET':
        return render(request, 'home/cadastrar.html')
    else:
        nome = request.POST.get("nome")
        sobrenome = request.POST.get("sobrenome")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        confirmar = request.POST.get("confirmar")
        cpf = request.POST.get("cpf")
        aniversario = request.POST.get("aniversario")
        # ------------------------------------------------------------------
        campos = [nome, sobrenome, email, senha, confirmar]
        for dado in campos:
            if len(dado.strip()) == 0:
                messages.add_message(request, constants.ERROR, 'Preencha todos os campos.')
                return render(request, 'home/cadastrar.html')
        email_aux = Usuario.objects.filter(email=email)
        if email_aux:
            messages.add_message(request, constants.ERROR, 'Já existe usuario cadastrado com esse email.')
            return render(request, 'home/cadastrar.html')
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos 6 caracteres.')
            return render(request, 'home/cadastrar.html')
        simbolos = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", ":", ";", "<",
                    "=",
                    ">", "?", "@", "[", "\\", "]", "^", "_", "`", "{", "|", "}", "~"]
        numeros = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        letras_upper = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "A", "S", "D", "F", "G", "H", "J", "K",
                        "L", "Z", "X", "C", "V", "B", "N", "M", "Ç"]
        letras_lower = list()
        for l in letras_upper:
            letras_lower.append(l.lower())
        # ----------------------------------------------------
        letras_lower_aux = False
        for ll in letras_lower:
            if senha.find(ll) != -1:
                letras_lower_aux = True
        simbolos_aux = False
        for s in simbolos:
            if senha.find(s) != -1:
                simbolos_aux = True
        letras_upper_aux = False
        for lu in letras_upper:
            if senha.find(lu) != -1:
                letras_upper_aux = True
        numeros_aux = False
        for nu in numeros:
            if senha.find(str(nu)) != -1:
                numeros_aux = True
        # ---------------------------------------------------
        if simbolos_aux == False:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos um caractere especial...')
            return render(request, 'home/cadastrar.htmll')
        if letras_upper_aux == False:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos uma letra maiúscula...')
            return render(request, 'home/cadastrar.html')
        if letras_lower_aux == False:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos uma letra minúscula...')
            return render(request, 'home/cadastrar.html')
        if numeros_aux == False:
            messages.add_message(request, constants.ERROR, 'A senha deve conter pelo menos um número...')
            return render(request, 'home/cadastrar.html')
        if senha != confirmar:
            messages.add_message(request, constants.ERROR, 'As senhas não correspondem.')
            return render(request, 'home/cadastrar.html')
        # ------------------------------------------------------------------
        try:
            usuario = Usuario.objects.create_user(
                first_name=nome,
                last_name=sobrenome,
                email=email,
                password=senha
            )
            cliente = Cliente(usuario=usuario, cpf=cpf, aniversario=aniversario)
            cliente.save()
            carrinho = Carrinho.objects.create(usuario=cliente)
            favorito = Favorito.objects.create(usuario=cliente)
            # MSG SUCESSO
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com sucesso.')
            return render(request, 'home/cadastrar.html')
        except:
            # MSG ERRO
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema.')
            return render(request, 'home/cadastrar.html')


def sair_view(request):
    logout(request)
    return redirect('/')
