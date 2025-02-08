# Carregando bibliotecas
import gc

import numpy as np
import tensorflow as tf

from carregar import aumentador_de_dados, carregar_dados
from chamadas import retorno_chamada, retorno_chamada_finetune
from constantes import EPOCA_AJUSTE_FINO, EPOCA_TREINAMENTO_INICIAL, PASTA_MODELO
from graficos import (
    avaliacao,
    espacador,
    exibir_array_previsoes,
    exibir_metricas,
    exibir_metricas_ajuste_fino,
    plotar_curva_roc,
)
from modelo import criar_modelo_base, criar_modelo_fine

# Limpar a memória e o cache do TensorFlow
tf.keras.backend.clear_session()
gc.collect()

# Verificar disponibilidade de TPU ou GPU e definir a estratégia de distribuição
try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    estrategia = tf.distribute.TPUStrategy(tpu)
    espacador('🔹 Estratégia de Distribuição com TPUs')
    print("TPU detectada e inicializada.")

except ValueError:
    estrategia = tf.distribute.get_strategy()
    if tf.config.list_physical_devices('GPU'):
        espacador('🔹 Estratégia de Distribuição com GPUs')
        print(f"GPU detectada: {tf.config.list_physical_devices('GPU')}")
    else:
        espacador('🔹 Estratégia de Distribuição com CPUs')
        print("Nenhuma GPU detectada. Usando CPU.\n")

# Carregar os dados de treino, teste e validação
dados_treino, dados_teste, dados_validacao = carregar_dados()

# Cria o callback para o modelo MobileNetV2
checkpoint_MobileNetV2, lr_reduction, early_stopping = retorno_chamada(
    PASTA_MODELO)

# Cria o callback para o ajuste fino do modelo MobileNetV2
checkpoint_finetune, lr_reduction_fine, early_stopping_fine = retorno_chamada_finetune(
    PASTA_MODELO)

################################### MobileNetV2 #######################################

# Cria o modelo base MobileNetV2 e treina
modelo, modelo_base = criar_modelo_base(
    estrategia, data_augmentation=aumentador_de_dados())

# Treinar Fase 1 - Congelado
espacador('🔹 Iniciando treinamento com camadas congeladas...')
history = modelo.fit(
    dados_treino,
    validation_data=dados_validacao,
    epochs=EPOCA_TREINAMENTO_INICIAL,
    callbacks=[checkpoint_MobileNetV2, early_stopping, lr_reduction],
)

# Avaliar o modelo com os dados de teste
avaliacao(modelo, dados_teste)

# Obter rótulos verdadeiros e previsões do modelo
y_verdadeiro = np.concatenate([y.numpy() for _, y in dados_teste])
y_pred_prob = modelo.predict(dados_teste)

# Plotar a Curva ROC
espacador('🔹 Plotar a Curva ROC MobileNetV2')
plotar_curva_roc(y_verdadeiro, y_pred_prob)

# Exibir as métricas de treinamento do modelo
acc = [0.] + history.history['accuracy']
val_acc = [0.] + history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

espacador('🔹 Histórico MobileNetV2')
exibir_metricas(acc, val_acc, loss, val_loss, 'MobileNetV2')

# # Gerar previsões para os dados de teste
predicoes = modelo.predict(dados_teste)

espacador('🔹 Probabilidade MobileNetV2')
exibir_array_previsoes(idx=0, y_pred=predicoes, dataset_teste=dados_teste)
print('\n')
exibir_array_previsoes(idx=31, y_pred=predicoes, dataset_teste=dados_teste)
espacador(largura_total=130)


########################## Ajuste Fino MobileNetV2 ##################################

# Fase 2: Fine-Tuning
espacador('🔹 Iniciando Ajuste Fino MobileNetV2...')
modelo = criar_modelo_fine(estrategia, modelo_base, modelo)
epoca_inicial = history.epoch[-1]

# Ajuste fino do modelo MobileNetV2
fine_tune_history = modelo.fit(
    dados_treino,
    validation_data=dados_validacao,
    epochs=EPOCA_AJUSTE_FINO + epoca_inicial,
    initial_epoch=epoca_inicial,
    callbacks=[checkpoint_finetune, early_stopping_fine, lr_reduction_fine],
)

# Avaliar o modelo com os dados de teste
avaliacao(modelo, dados_teste)

# Obter rótulos verdadeiros e previsões do modelo
y_verdadeiro = np.concatenate([y.numpy() for _, y in dados_teste])
y_pred_prob = modelo.predict(dados_teste)

# Plotar a Curva ROC
espacador('🔹 Plotar a Curva ROC Ajuste Fino MobileNetV2')
plotar_curva_roc(y_verdadeiro, y_pred_prob)

# Exibir as métricas de treinamento do modelo
acc += fine_tune_history.history['accuracy']
val_acc += fine_tune_history.history['val_accuracy']
loss += fine_tune_history.history['loss']
val_loss += fine_tune_history.history['val_loss']

espacador('🔹 Histórico Ajuste Fino MobileNetV2')
exibir_metricas_ajuste_fino(
    acc, val_acc, loss, val_loss, epoca_inicial, 'Ajuste Fino MobileNetV2')

# Gerar previsões para os dados de teste
predicoes = modelo.predict(dados_teste)

espacador('🔹 Probabilidade Ajuste Fino MobileNetV2')
exibir_array_previsoes(idx=0, y_pred=predicoes, dataset_teste=dados_teste)
print('\n')
exibir_array_previsoes(idx=31, y_pred=predicoes, dataset_teste=dados_teste)

espacador('🔹 FINAL ETAPA AJUSTE FINO MOBILENETV2 🔹', largura_total=130)
################################################################################
