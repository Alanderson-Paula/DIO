import tensorflow as tf
from constantes import SEMENTE, TAMANHO_DO_LOTE, TAMANHO_IMG
from graficos import espacador

AUTOTUNE = tf.data.AUTOTUNE

# Função para pré-processar as imagens
def preprocessar(imagem:tf.Tensor, rotulo:tf.Tensor):
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

    data_augmentation = tf.keras.Sequential()
    data_augmentation.add(tf.keras.layers.RandomFlip('horizontal'))
    data_augmentation.add(tf.keras.layers.RandomRotation(0.2))
    data_augmentation.add(tf.keras.layers.RandomZoom(0.2))
    data_augmentation.add(tf.keras.layers.RandomContrast(0.2))
    data_augmentation.add(tf.keras.layers.RandomTranslation(0.2, 0.2))
    data_augmentation.add(tf.keras.layers.RandomHeight(0.2))
    data_augmentation.add(tf.keras.layers.RandomWidth(0.2))
    data_augmentation.add(tf.keras.layers.RandomBrightness(0.2))
    data_augmentation.add(tf.keras.layers.RandomFlip("vertical"))

    return data_augmentation

# Carregar os dados de treino, teste e validação
def carregar_dados(pasta_treino:str, pasta_validacao:str, pasta_teste:str):
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
    espacador('Dados de Treino')
    dados_treino = tf.keras.preprocessing.image_dataset_from_directory(
        pasta_treino,
        image_size=TAMANHO_IMG,
        batch_size=TAMANHO_DO_LOTE,
        shuffle=True,
        seed=SEMENTE,
    )

    dados_validacao = tf.keras.preprocessing.image_dataset_from_directory(
        pasta_validacao,
        image_size=TAMANHO_IMG,
        batch_size=TAMANHO_DO_LOTE,
        shuffle=False

    )

    dados_teste = tf.keras.preprocessing.image_dataset_from_directory(
        pasta_teste,
        image_size=TAMANHO_IMG,
        batch_size=TAMANHO_DO_LOTE,
        shuffle=False

    )
    espacador('Dados de Treino')

    # Melhorar desempenho do pipeline de dados com cache e prefetch
    dados_treino = dados_treino.map(preprocessar, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)
    dados_validacao = dados_validacao.map(preprocessar, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)
    dados_teste = dados_teste.map(preprocessar, num_parallel_calls=AUTOTUNE).prefetch(AUTOTUNE)


    return dados_treino, dados_teste, dados_validacao
