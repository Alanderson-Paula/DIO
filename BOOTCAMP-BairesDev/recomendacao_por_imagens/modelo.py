import tensorflow as tf
from constantes import (  # EPOCA_TREINAMENTO_INICIAL,; NUM_CLASSES,
    AJUSTE_FINO,
    CAMADA_ESCONDIDA,
    DROPOUT,
    FORMA_ENTRADA,
    TAXA_APRENDIZAGEM,
)
from graficos import espacador


# Criar o modelo base MobileNetV2 (pré-treinado no ImageNet)
def criar_modelo_base(estrategia, data_augmentation):
    """
    #### Cria o modelo base MobileNetV2 com as camadas adicionais

    Argumentos:
            estrategia: Estratégia de distribuição
            data_augmentation: aumentador de dados

    Retorno:
            modelo: Modelo base MobileNetV2
    """
    with estrategia.scope():
        modelo_base = tf.keras.applications.MobileNetV2(include_top=False, weights='imagenet', input_shape=FORMA_ENTRADA)

        modelo_base.trainable = False

        entradas = tf.keras.Input(shape=FORMA_ENTRADA, name="entrada")
        x = data_augmentation(entradas)
        x = modelo_base(x, training=False)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dropout(DROPOUT)(x)
        x = tf.keras.layers.Dense(CAMADA_ESCONDIDA, activation="relu")(x)
        # x = tf.keras.layers.BatchNormalization()(x)

        modelo = tf.keras.models.Model(inputs=entradas, outputs=x)

        modelo = compilar_modelo(modelo, estrategia)

    return modelo, modelo_base

def compilar_modelo(modelo, estrategia):
    """
    #### Compilar o modelo

    Argumentos:
            modelo: Modelo a ser compilado
            estrategia: Estratégia de distribuição

    Retorno:
            modelo: Modelo compilado
    """
    with estrategia.scope():
        modelo.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=TAXA_APRENDIZAGEM),
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        espacador('Sumário Modelo Base MobileNetV2')
        modelo.summary(show_trainable=True, expand_nested=True)
        espacador('Treinamento do Modelo Base MobileNetV2')

    return modelo


def criar_modelo_fine(estrategia, modelo_base, modelo):
    """
    #### Cria o modelo para ajuste fino

    Argumentos:
            estrategia: Estratégia de distribuição
            modelo_base: Modelo base MobileNetV2
            modelo: Modelo base MobileNetV2 com camadas adicionais

    Retorno:
            modelo: Modelo para ajuste fino
    """
    with estrategia.scope():
        modelo_base.trainable = True
        for layer in modelo_base.layers[:AJUSTE_FINO]:  # Descongela ms camadas
            layer.trainable = False

        modelo.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"],
        )

    return modelo
