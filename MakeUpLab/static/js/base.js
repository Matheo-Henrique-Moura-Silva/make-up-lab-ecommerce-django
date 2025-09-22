document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript da Beleza Chic carregado!');

    const adicionarAoCarrinhoBtns = document.querySelectorAll('.js-adicionar-item');

    adicionarAoCarrinhoBtns.forEach(button => {
        button.addEventListener('click', function() {
            const produtoId = this.dataset.produtoId;
            const urlBase = this.dataset.urlAdicionar;

            const quantidadeProdutoInput = this.closest('.product-card').querySelector('.js-quantidade-produto');

            if (!quantidadeProdutoInput) {
                console.error("Input de quantidade não encontrado para o produto:", produtoId);
                alert("Erro: Quantidade do produto não pode ser determinada.");
                return;
            }

            const quantidade = quantidadeProdutoInput.value;

            if (!urlBase) {
                console.error("Atributo data-url-adicionar não encontrado no botão.");
                alert("Erro interno: URL de adição não configurada.");
                return;
            }

            let urlConstruida = urlBase.replace('0', produtoId); // Substitui o primeiro 0 pelo ID
            urlConstruida = urlConstruida.replace('0', quantidade); // Substitui o segundo 0 pela quantidade

            fetch(urlConstruida)
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(err => {
                            throw new Error(err.message || 'Erro na requisição');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        console.log(status);
                        alert(data.message);
                        window.location.reload();
                    } else if (data.status === 'error') {
                        console.error(status);
                        alert(data.message);
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Erro ao adicionar item:', error);
                    alert("A quantidade deve ser maior ou igual a 1!");
                    setTimeout(() => {
                        window.location.reload();
                        }, 5000);
                });
        });
    });

    const botoesEditar = document.querySelectorAll('.js-editar-item');

    // Itera sobre cada botão encontrado
    botoesEditar.forEach(botao => {
        // Adiciona um ouvinte de evento 'click' a cada botão
        botao.addEventListener('click', function(event) {
            // Previne o comportamento padrão do formulário, que é recarregar a página
            event.preventDefault();

            // 1. Obtém o ID do item a partir do atributo data-item-id
            const itemId = this.getAttribute('data-item-id');

            // 2. Encontra o modal pai para obter os dados do formulário
            const modal = this.closest('.modal');

            // 3. Seleciona o campo de input dentro do modal
            const inputQuantidade = modal.querySelector('.js-quantidade-item');
            const novaQuantidade = inputQuantidade.value;

            // 4. Obtém a URL de edição do atributo data-url-editar
            const urlEditarBase = this.getAttribute('data-url-editar');

            // 5. Substitui os placeholders na URL com os valores corretos
            // Ex: /editar_item/0/0/ vira /editar_item/123/5/
            let urlConstruida = urlEditarBase.replace('0', itemId); // Substitui o primeiro 0 pelo ID
            urlConstruida = urlConstruida.replace('0', novaQuantidade); // Substitui o segundo 0 pela quantidade

            fetch(urlConstruida)
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(err => {
                            throw new Error(err.message || 'Erro na requisição');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        console.log(status);
                        alert(data.message);
                        const modalInstance = bootstrap.Modal.getInstance(modal);
                        modalInstance.hide();
                        window.location.reload();
                    } else if (data.status === 'error') {
                        console.error(status);
                        alert(data.message);
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Erro ao editar o item:', error);
                    alert("Faça login para adicionar produto ao carrinho!");
                    setTimeout(() => {
                        window.location.reload();
                        }, 5000);
                });
        });
    });
    const adicionarAoFavoritoBtns = document.querySelectorAll('.js-adicionar-favorito');

    adicionarAoFavoritoBtns.forEach(button => {
        button.addEventListener('click', function() {
            const urlConstruida = this.dataset.urlAdicionar;
            console.log(urlConstruida)

            fetch(urlConstruida)
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(err => {
                            throw new Error(err.message || 'Erro na requisição');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.status === 'success') {
                        console.log(status);
                        alert(data.message);
                        window.location.reload();
                    } else if (data.status === 'error') {
                        console.error(status);
                        alert(data.message);
                        window.location.reload();
                    }
                })
                .catch(error => {
                    console.error('Erro ao adicionar item:', error);
                    alert("Faça login para adicionar produto ao carrinho!");
                    setTimeout(() => {
                        window.location.reload();
                        }, 5000);
                });
        });
    });

});
