import os

import matplotlib.pyplot as plt
from constantes import ESPACOS, PASTA_MODELO, TAMANHO_FIGURA
from PIL import Image, ImageOps


# Função para exibir as métricas de treinamento
def exibir_metricas(acc, val_acc, loss, val_loss, nome_modelo) -> None:
    """
    ##### Exibir as métricas de treinamento do modelo
    Arguemntos:
        acc: Precisão no treinamento
        val_acc: Precisão na validação
        loss: Perda no treinamento
        val_loss: Perda na validação
        nome_modelo: Nome do modelo

    Retorna:  None
        """
    fig = plt.figure(figsize=(14,5))

    # Plotar a acurácia
    ax = fig.add_subplot(1,2,1)
    ax.plot(acc, label='Precisão no treinamento')
    ax.plot(val_acc, label='Precisão na validação')
    ax.legend(loc='lower right')
    ax.set_ylabel('Precisão')
    ax.set_ylim([min(ax.set_ylim()),1])
    ax.set_title(f'Precisão de treinamento e validação {nome_modelo}')
    ax.set_xlabel('época')

    # Plotar a perda (loss)
    ax2 = fig.add_subplot(1,2,2)
    ax2.plot(loss, label='Perda de treinamento')
    ax2.plot(val_loss, label='Perda de validação')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Entropia Cruzada')
    ax2.set_ylim([0,1.0])
    ax2.set_title(f'Perda de treinamento e validação {nome_modelo}')
    ax2.set_xlabel('época')

    # salvar imagem pasta modelo
    #plt.savefig(f'{PASTA_MODELO}{nome_modelo}.png')

    plt.show()

# Função para exibir as métricas de treinamento
def exibir_metricas_ajuste_fino(acc, val_acc, loss, val_loss, epoca_inicial, nome_modelo) -> None:
    """
    ##### Exibir as métricas de treinamento do modelo
    Arguemntos:
        acc: Precisão no treinamento
        val_acc: Precisão na validação
        loss: Perda no treinamento
        val_loss: Perda na validação
        epoca_inicial: Época inicial do ajuste fino
        nome_modelo: Nome do modelo
    Retorna:  None
        """
    fig = plt.figure(figsize=TAMANHO_FIGURA)

    # Plotar a acurácia
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Precisão no treinamento')
    plt.plot(val_acc, label='Precisão na validação')
    plt.ylim([0, 1])
    plt.plot([epoca_inicial-1,epoca_inicial-1],
              plt.ylim(), label='Inicio do ajuste fino')
    plt.legend(loc='lower right')
    plt.title(f'Precisão de treinamento e validação {nome_modelo}')


    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Perda de treinamento')
    plt.plot(val_loss, label='Perda de validação')

    plt.ylim([0, 1.0])
    plt.plot([epoca_inicial-1,epoca_inicial-1],
            plt.ylim(), label='Inicio do ajuste fino')
    plt.legend(loc='upper right')
    plt.title(f'Perda de treinamento e validação {nome_modelo}')
    plt.xlabel('época')

    # salvar imagem pasta modelo
    # plt.savefig(f'{PASTA_MODELO}{nome_modelo}.png')

    plt.show()

# Função para adicionar um separador visual
def espacador(titulo:str = None, largura_total:int = ESPACOS):
    """
    #### Adiciona um separador visual com um título opcional.

    Argumentos:
        titulo: Título do separador
        largura_total: Largura total do separador (padrão: 160)

    Retorna: None
    """
    if titulo is not None:
        tamanho_titulo = len(titulo)
        espacos_laterais = (largura_total - tamanho_titulo - 2) // 2
        espacos_restantes = largura_total - (espacos_laterais * 2) - tamanho_titulo - 2
        print("\n" + "#" * espacos_laterais + f" {titulo} " + "#" * (espacos_laterais + espacos_restantes) + "\n")
    else:
        print("\n" + "#" * largura_total + "\n")

# Função para avaliar o modelo
def avaliacao(modelo, dados_teste):
    """
    #### Avalia o modelo com os dados de teste.

    Argumentos:
        modelo: Modelo treinado
        dados_teste: Dados de teste

    Retorna: None
    """
    espacador('Avaliação do Modelo', 160)
    test_loss, test_acc = modelo.evaluate(dados_teste)
    print(f'Teste de perda:, {test_loss:.2f}')
    print(f'Teste acurácia:, {test_acc:.2f}')

# Função para exibir recomendações de produtos similares ao produto selecionado
def exibir_recomendacoes(opcao_usuario, imagens_similares):
    """
    #### Exibe recomendações de produtos similares.

    Argumentos:
        opcao_usuario: Caminho da imagem selecionada pelo usuário
        imagens_similares: Lista de tuplas contendo o caminho da imagem e a similaridade

    Retorna: None

    """
    plt.figure(figsize=(18, 6))
    try:
        img = Image.open(opcao_usuario)
        img_com_borda = ImageOps.expand(img, border=2, fill='black')
        plt.subplot(1, len(imagens_similares) + 1, 1)
        plt.imshow(img_com_borda)
        plt.title('Selecionado')
        plt.axis('off')

        for i, (produto, similaridade) in enumerate(imagens_similares):
            try:
                img = Image.open(produto)
                plt.subplot(1, len(imagens_similares) + 1, i + 2)
                plt.imshow(img)
                plt.title(f'{os.path.basename(produto)} - {int(similaridade*100)}%')
                plt.axis('off')
            except Exception as e:
                print(f"Erro ao carregar imagem {produto}: {e}")
                continue

        plt.show()
    except Exception as e:
        print(f"Erro ao exibir recomendacoes: {e}")

