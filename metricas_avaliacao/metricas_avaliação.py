# -*- coding: utf-8 -*-

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import PIL
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import tensorflow as tf
from keras.applications.imagenet_utils import preprocess_input
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
# from keras.preprocessing import image
from keras.utils import load_img, img_to_array
# from matplotlib.pyplot import imshow
from PIL import Image, ImageFile
from sklearn.metrics import auc, roc_curve
from sklearn.model_selection import train_test_split
from tensorflow.keras import datasets, layers, models

# Detectar e conectar à TPU
try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()  # Detecta TPU
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    estrategia = tf.distribute.TPUStrategy(tpu)                # Estratégia de distribuição
    print("TPU inicializada.")
except ValueError:
    estrategia = tf.distribute.get_strategy()                  # Usar estratégia de distribuição padrão
    print("Nenhuma TPU disponível.")


os.chdir('/caminho_da_pasta_com_diretorios/')

root = 'Annonaceae' # pasta com os diretórios de cada classes
categorias = [x[0] for x in os.walk(root) if x[0]][1:]
nome_das_classes = [os.path.basename(c) for c in categorias]

print(categorias)

def matriz_confusao(df_matriz_conf, nome_classes):
    if df_matriz_conf.shape[0] != df_matriz_conf.shape[1]:
        raise ValueError("A matriz deve ser quadrada!")

    fig = go.Figure(
        data=go.Heatmap(
            z=df_matriz_conf,
            x=nome_classes,
            y=nome_classes,
            colorscale="Blues",
            hoverongaps=False,
            text=df_matriz_conf.astype(str),
            texttemplate="%{text}",
        )
    )

    fig.update_layout(
        title="Matriz de Confusão",
        title_x = 0.5,
        xaxis_title="Predições",
        yaxis_title="Valores Reais",
        yaxis=dict(
            tickmode="array",
            tickvals=np.arange(len(nome_classes)),
            ticktext=nome_classes,
            autorange='reversed',
            tickangle=90,
            title_font=dict(size=14)
        ),

        xaxis=dict(
            tickmode="array",
            tickvals=np.arange(len(nome_classes)),
            ticktext=nome_classes,
            title_font=dict(size=14)
        ),
        width=400,
        height=400,
        margin=dict(l=10, r=10, t=30, b=10),
        showlegend=False,
        autosize=False,
        paper_bgcolor="white",
        plot_bgcolor="white"

    )

    vp = df_matriz_conf.iloc[0, 0]
    vn = df_matriz_conf.iloc[1, 1]
    fp = df_matriz_conf.iloc[1, 0]
    fn = df_matriz_conf.iloc[0, 1]
    n  = vp+vn+fp+fn

    sensibilidade  = round(vp/(vp+fn), 2)
    especificidade = round(vn/(fp+vn), 2)
    acuracia       = round((vp+vn)/n, 2)
    precisao       = round(vp/(vp+fp), 2)

    if precisao + sensibilidade > 0:
        f_score = round(2 * (precisao * sensibilidade) / (precisao + sensibilidade), 2)
    else:
        f_score = 0.0

    print("Métricas de Classificação:")
    print("Accuracy       =", acuracia)
    print("Precision      =", precisao)
    print("Recall         =", sensibilidade)
    print("Especificidade =", especificidade)
    print("f1 score       =", f_score)
    print(' ')

    fig.show()

def curva_roc(y_true, y_scores):
    print('')
    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines',
                             line=dict(color='blue', width=2),
                             name=f'Curva ROC (AUC = {roc_auc:.2f})'))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines',
                             line=dict(color='gray', width=1, dash='dash'),
                             showlegend=False))

    fig.update_layout(title='Curva ROC',
                      xaxis_title='Taxa de Falsos Positivos (FPR)',
                      yaxis_title='Taxa de Verdadeiros Positivos (TPR)',
                      legend=dict(x=0.7, y=0.1),
                      width=400, height=400)
    fig.show()


def carregar_imagem(pasta):
    try:
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        img = load_img(pasta, target_size=(224, 224))
        x = img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        return img, x
    except PIL.UnidentifiedImageError:
        print(f"Ignorando imagem corrompida: {pasta}")
        return None, None

# carregando as imagens e redimensionando
dados = []
for c, categoria in enumerate(categorias):
    aimgens = [os.path.join(dp, f) for dp, dn, nome_arquivos
              in os.walk(categoria) for f in nome_arquivos
              if os.path.splitext(f)[1].lower() in ['.jpg','.png','.jpeg', '.jfif']]
    for img_path in aimgens:
        img, x = carregar_imagem(img_path)
        if img is not None and x is not None:
            dados.append({'x':np.array(x[0]), 'y':c})
        else:
            aimgens.remove(img_path)
            os.remove(img_path)

num_classes = len(categorias)

# separando e normalizandoos dados
y = np.array([item['y'] for item in dados])
x = np.array([item['x'] for item in dados])

x_treino, x_rem, y_treino, y_rem = train_test_split(x, y, train_size=0.7, random_state=42)
x_teste, x_validacao, y_teste, y_validacao = train_test_split(x_rem, y_rem, test_size=0.5, random_state=42)

y_treino = tf.keras.utils.to_categorical(y_treino, num_classes=num_classes)
y_validacao = tf.keras.utils.to_categorical(y_validacao, num_classes=num_classes)
y_teste = tf.keras.utils.to_categorical(y_teste, num_classes=num_classes)

x_treino = x_treino.astype('float32') / 255.
x_validacao = x_validacao.astype('float32') / 255.
x_teste = x_teste.astype('float32') / 255.

print()
print("x_treino shape:   ", x_treino.shape)
print("y_treino shape:   ", y_treino.shape)
print("x_teste shape:    ", x_teste.shape)
print("y_teste shape:    ", y_teste.shape)
print("x_validacao shape:", x_validacao.shape)
print("y_validacao shape:", y_validacao.shape)

# criando o modelo
with estrategia.scope():
    print("Entradas: ", x_treino.shape[1:])

    modelo = models.Sequential()
    modelo.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)))
    modelo.add(layers.MaxPooling2D((2, 2)))

    modelo.add(layers.Conv2D(64, (3, 3), activation='relu'))
    modelo.add(layers.MaxPooling2D((2, 2)))

    modelo.add(layers.Dropout(0.25))

    modelo.add(layers.Conv2D(128, (3, 3), activation='relu'))
    modelo.add(layers.MaxPooling2D((2, 2)))

    modelo.add(layers.Conv2D(64, (3, 3), activation='relu'))
    modelo.add(layers.MaxPooling2D((2, 2)))

    modelo.add(layers.Conv2D(32, (3, 3), activation='relu'))
    modelo.add(layers.MaxPooling2D(pool_size=(2, 2)))

    modelo.add(layers.Dropout(0.25))

    modelo.add(layers.Flatten())
    modelo.add(layers.Dense(32, activation='relu'))
    modelo.add(layers.Dense(num_classes, activation='softmax'))

    modelo.summary()

# treinando o modelo
optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True)

reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    patience=5,
    min_lr=1e-6)

modelo.compile(optimizer=optimizer,
              loss='categorical_crossentropy',
              metrics=['accuracy'])

modelo.fit(x=x_treino,
          y=y_treino,
          epochs=50,
          batch_size=128,
          validation_data=(
              x_validacao, y_validacao),
          callbacks=[
              early_stopping, reduce_lr,]
          )

perda, acuracia = modelo.evaluate(x_teste, y_teste, verbose=0, batch_size=128)
print(f'Teste de perda:, {perda:.2f}')
print(f'Teste acurácia:, {acuracia:.2f}')

#predições do modelo
predicoes = modelo.predict(x_teste)
y_scores = predicoes[:, 1]

# preparando os dados para plotar no plotly
y_teste_labels = np.argmax(y_teste, axis=1)
y_pred_labels = np.argmax(predicoes, axis=1)

con_mat = tf.math.confusion_matrix(labels=y_teste_labels, predictions=y_pred_labels).numpy()
con_mat_norm = np.around(con_mat.astype('float') / con_mat.sum(axis=1)[:, np.newaxis], decimals=2)
con_mat_df = pd.DataFrame(con_mat_norm,
                index = nome_das_classes ,
                            columns = nome_das_classes )


# plot matriz e curva
matriz_confusao(con_mat_df, nome_das_classes )

curva_roc(y_teste_labels, y_scores)
