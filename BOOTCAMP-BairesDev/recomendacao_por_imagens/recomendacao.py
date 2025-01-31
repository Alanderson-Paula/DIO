import os

import numpy as np
from constantes import TAMANHO_IMG
from graficos import espacador, exibir_recomendacoes
from PIL import Image

# from sklearn.metrics.pairwise import cosine_similarity
from tensorflow.keras.models import Model  # type: ignore

cache_caracteristicas = {}


def recomendar_produtos_similares(pasta_treino:str, caminho_imagem:str, modelo_extrator, cache_caracteristicas:dict)-> list:
    """
    #### Recomenda produtos similares com base na similaridade de cosseno.

    Argumentos:
        pasta_treino: (str), caminho da pasta de treino.
        caminho_imagem: (str), caminho da imagem de consulta.
        modelo_extrator: modelo Keras para extrair características.
        cache_caracteristicas: dict, cache de características de imagens.

    Retorna:
        list: lista de tuplas (caminho, similaridade) para os produtos mais similares.
    """
    if not cache_caracteristicas:
        print("Carregando características das imagens...")
        # Carregar características de todas as imagens de treino e armazenar em cache para uso futuro (evita recálculo)
        cache_caracteristicas.update(carregar_caracteristicas(pasta_treino, modelo_extrator))

    # Extrair características da imagem de consulta
    try:
        caracteristicas_consulta = extrair_caracteristicas(caminho_imagem, modelo_extrator)
        if caracteristicas_consulta is None:
            return []
        # Calcular similaridade de cosseno entre a imagem de consulta e todas as imagens de treino
        similaridades = {
            caminho: calcular_similaridade(caracteristicas_consulta, caracteristicas)
            for caminho, caracteristicas in cache_caracteristicas.items()
        }
        # Ordenar por similaridade e retornar os 3 produtos mais similares
        produtos_similares = sorted(similaridades.items(), key=lambda x: x[1], reverse=True)[:3]
        return produtos_similares
    except Exception as e:
        print(f"Erro ao recomendar produtos: {e}")
        return []


def exibir_recomendacao_pasta(pasta_teste:str, pasta_treino:str, modelo_extrator, cache_caracteristicas:dict):
    """
    #### Exibe recomendações para todas as imagens em uma pasta de teste.

    Argumentos:
        pasta_teste: (str), caminho da pasta de teste.
        pasta_treino: (str), caminho da pasta de treino.
        modelo_extrator: modelo Keras para extrair características.
        cache_caracteristicas: dict, cache de características de imagens.

    Retorna:
        None
    """
    # Percorrer todas as subpastas e arquivos da pasta de teste e exibir recomendações
    for raiz, dirs, arquivos in os.walk(pasta_teste):
        nome_pasta = os.path.basename(raiz).replace('_', ' ').title()
        espacador(nome_pasta, 160)
        for arquivo in arquivos:
            if arquivo.endswith('.jpg'):
                caminho_arquivo = os.path.join(raiz, arquivo)
                produtos_similares = recomendar_produtos_similares(pasta_treino, caminho_arquivo, modelo_extrator, cache_caracteristicas)
                exibir_recomendacoes(caminho_arquivo, produtos_similares)


def calcular_similaridade(caracteristicas1:np.array, caracteristicas2:np.array) -> float:
    """
    #### Calcula a similaridade entre duas listas de características.

    Argumentos:
        caracteristicas1: np.array, características da primeira imagem.
        caracteristicas2: np.array, características da segunda imagem.

    Retorna:
        float: similaridade de cosseno entre as características.
    """
    # return cosine_similarity([caracteristicas1], [caracteristicas2])[0][0]
    caracteristicas1 = caracteristicas1 / np.linalg.norm(caracteristicas1)
    caracteristicas2 = caracteristicas2 / np.linalg.norm(caracteristicas2)
    return np.dot(caracteristicas1, caracteristicas2)

def criar_caracteristicas_extrator(pasta_treino:str, modelo_base) -> tuple:
    """
    #### Carregar carcteristicas e criar modelo extrator.

    Argumentos:
        pasta_treino: (str), caminho da pasta de treino.
        modelo_base: modelo Keras base.

    Retorna:
        modelo_extrator: modelo Keras para extrair características.
        cache_caracteristicas: dict, cache de características de imagens.

    """
    modelo_extrator = Model(inputs=modelo_base.input, outputs=modelo_base.get_layer("global_average_pooling2d").output)
    cache_caracteristicas.update(carregar_caracteristicas(pasta_treino, modelo_extrator))
    return modelo_extrator, cache_caracteristicas

def carregar_caracteristicas(pasta:str, modelo_extrator:Model ) -> dict:
    """
    #### Carrega características de todas as imagens de uma pasta.

    Argumenos:
            pasta: (str), caminho da pasta com as imagens.
            modelo_extrator: modelo Keras para extrair características.

    Retorna:
            dict: dicionário com caminho do arquivo -> características.
    """
    caracteristicas = {}
    for classe in os.listdir(pasta):
        caminho_classe = os.path.join(pasta, classe)
        if not os.path.isdir(caminho_classe):
            continue
        for arquivo in os.listdir(caminho_classe):
            caminho_arquivo = os.path.join(caminho_classe, arquivo)
            try:
                caracteristicas[caminho_arquivo] = extrair_caracteristicas(caminho_arquivo, modelo_extrator)
            except Exception as e:
                print(f"Erro ao processar {caminho_arquivo}: {e}")
    return caracteristicas


def extrair_caracteristicas(caminho_imagem:str, modelo_extrator) -> np.array:
    """
    #### Extrai características de uma imagem usando o modelo fornecido.

    Argumentos:
        caminho_imagem: (str), caminho da imagem.
        modelo_extrator: modelo Keras para extrair características.

    Retorna:
        np.array: características da imagem.
    """
    try:
        img = Image.open(caminho_imagem).resize(TAMANHO_IMG)
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        caracteristicas = modelo_extrator.predict(img_array)
        return caracteristicas.flatten()
    except Exception as e:
        print(f"Erro ao carregar imagem {caminho_imagem}: {e}")
        return None
