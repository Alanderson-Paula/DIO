import os

import matplotlib.pyplot as plt
import numpy as np

fotos = os.listdir('img')


def binarizar(img, limiar=127):
    """
    #### Binariza uma imagem, convertendo seus valores de pixel para 0 ou 1 com base em um limiar fornecido.

    A função percorre cada pixel da imagem, convertendo-o para 0 (preto) se o valor do pixel for inferior
    ao limiar especificado e para 1 (branco) caso contrário. Isso é útil para segmentar objetos em uma imagem
    ou realizar outras operações de processamento de imagem.

    Parâmetros:
    img (ndarray): Imagem de entrada, que deve ser uma matriz de pixels (geralmente uma imagem em tons de cinza).
    limiar (int, opcional): Valor de limiar para binarização. Qualquer valor de pixel abaixo deste limiar será
    convertido para 0, e valores acima ou iguais serão convertidos para 1. O valor padrão é 127.

    Retorna:
    ndarray: Imagem binarizada, onde os pixels são 0 ou 1.
    """

    canal_cinza = img[:, :, ]
    img_binaria = np.zeros((canal_cinza.shape[0], canal_cinza.shape[1]))
    for linha in range(canal_cinza.shape[0]):
        for coluna in range(canal_cinza.shape[1]):
            if canal_cinza[linha][coluna] < limiar:
                img_binaria[linha][coluna] = 0
            else:
                img_binaria[linha][coluna] = 1

    return img_binaria


def plot_imagens(img, cinza, binaria):
    """
    #### Plota três imagens lado a lado: a imagem original, a imagem em tons de cinza e a imagem binarizada.
    ---

    A função cria uma figura com três subgráficos, exibindo as imagens nas posições correspondentes. Isso permite
    uma visualização comparativa dos diferentes estágios do processamento de uma imagem.

    Parâmetros:
    img (ndarray): Imagem original que será exibida no primeiro subgráfico.
    cinza (ndarray): Imagem em tons de cinza que será exibida no segundo subgráfico.
    binaria (ndarray): Imagem binarizada que será exibida no terceiro subgráfico.

    Retorna:
    None: A função apenas exibe as imagens, sem retornar nada.
    """

    plt.figure(figsize=(10, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(img)
    plt.title("Imagem original")

    plt.subplot(1, 3, 2)
    plt.imshow(cinza, cmap=plt.get_cmap("gray"))
    plt.title("Imagem tons de cinza")

    plt.subplot(1, 3, 3)
    plt.imshow(binaria, cmap=plt.get_cmap("gray"))
    plt.title("Imagem Binaria")
    plt.show()


for foto in fotos:
    img = plt.imread(f'img/{foto}')

    # separa os canais da imagem
    vermelho = img[:, :, 0]
    verde = img[:, :, 1]
    azul = img[:, :, 2]

    # converter a imagem para tons de cinza
    img_cinza = 0.2126 * vermelho + 0.7152 * verde + 0.0722 * azul

    # cria uma imagen binária
    img_binaria = binarizar(img_cinza, 127)

    # Exibe as imagens agrupadas
    plot_imagens(img, img_cinza, img_binaria)
