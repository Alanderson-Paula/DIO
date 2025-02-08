# import os

from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from constantes import (
    CLASSES,
    PASTA_TESTE,
    PASTA_TREINO,
    PASTA_VALIDACAO,
    SEMENTE,
    TAMANHO_DO_LOTE,
    TAMANHO_IMG,
)
from graficos import espacador, plotar_distribuicao_classes

AUTOTUNE = tf.data.AUTOTUNE


# Função para pré-processar as imagens
def preprocessar(imagem: tf.Tensor, rotulo: tf.Tensor):
    """
    #### Normalizar e redimensionar as imagens

    Argumentos:
            imagem (tf.Tensor): Imagem a ser pré-processada
            rotulo (tf.Tensor): Rótulo correspondente à imagem

    Retorno:
            tf.Tensor: Imagem normalizada e redimensionada
            tf.Tensor: Rótulo
    """
    return tf.keras.applications.mobilenet_v2.preprocess_input(imagem), rotulo


# Criar a função de data augmentation
def aumentador_de_dados():
    """
    #### Data augmentation para o conjunto de treino

    Retorna:
            tf.keras.Sequential: Camada de data augmentation
    """
    return tf.keras.Sequential([
        tf.keras.layers.RandomFlip('horizontal'),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.2),
        tf.keras.layers.RandomContrast(0.2),
        tf.keras.layers.RandomTranslation(0.2, 0.2)
    ])


# Função para contar as classes
def contar_classes(dataset):
    """
    #### Conta a distribuição das classes no dataset.

    Argumentos:
            dataset: Conjunto de dados

    Retorno:
            contagem: Quantidade de rótulos
    """
    rotulos = np.concatenate([y.numpy() for _, y in dataset])
    contagem = Counter(rotulos)

    print("Distribuição das Classes:")
    for classe, qtd in contagem.items():
        print(f"{CLASSES[classe].replace('_', ' ').title()}: {qtd} imagens")
        
    print('\n')
    return contagem


# Carregar os dados de treino, teste e validação
def carregar_dados():
    """
    #### Carregar dados de treino, validação e teste

    Argumentos:
            pasta_treino (str): Caminho para a pasta de treino
            pasta_validacao (str): Caminho para a pasta de validação
            pasta_teste (str): Caminho para a pasta de teste

    Retorna:
            tf.data.Dataset: Dados de treino
            tf.data.Dataset: Dados de teste
            tf.data.Dataset: Dados de validação

            """
    espacador('🔹 Dados de Treino')

    dados_treino = tf.keras.preprocessing.image_dataset_from_directory(
        PASTA_TREINO,
        image_size=TAMANHO_IMG,
        batch_size=TAMANHO_DO_LOTE,
        shuffle=True,
        seed=SEMENTE,
        class_names=CLASSES
    )

    dados_validacao = tf.keras.preprocessing.image_dataset_from_directory(
        PASTA_VALIDACAO,
        image_size=TAMANHO_IMG,
        batch_size=TAMANHO_DO_LOTE,
        shuffle=False,
        class_names=CLASSES

    )

    dados_teste = tf.keras.preprocessing.image_dataset_from_directory(
        PASTA_TESTE,
        image_size=TAMANHO_IMG,
        batch_size=TAMANHO_DO_LOTE,
        shuffle=False,
        class_names=CLASSES

    )

    # Contagem inicial das classes (antes do augmentation)
    # espacador("🔹istribuição de Classes - SEM AUGMENTATION:")
    # contagem_original = contar_classes(dados_treino)
    # print('\n')

    # # Aplicar Data Augmentation
    # aumento = aumentador_de_dados()
    # dados_treino = dados_treino.map(lambda x, y: (aumento(x, training=True), y))

    # espacador('🔹 Dados de Treino')

    # Melhorar desempenho do pipeline de dados com cache e prefetch
    dados_treino = dados_treino.map(
        preprocessar, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)
    dados_validacao = dados_validacao.map(
        preprocessar, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)
    dados_teste = dados_teste.map(
        preprocessar, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)

    # Contagem das imagens das classes
    espacador("🔹 Distribuição de Imagens por Classes ")
    contagem_original = contar_classes(dados_treino)
    # print('\n')

    # espacador('🔹 Analisar distribuição das classes')

    # Analisar distribuição das classes
    # classes_treino = np.concatenate([y.numpy() for _, y in dados_treino])
    # unique, counts = np.unique(classes_treino, return_counts=True)
    # print(f"Distribuição das Classes (Treino): {dict(zip(unique, counts))}\n")

    # Plotar distribuição das classes
    plotar_distribuicao_classes(contagem_original)

    return dados_treino, dados_teste, dados_validacao
