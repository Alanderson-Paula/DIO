# Carregando bibliotecas
import gc

import tensorflow as tf
from carregar import aumentador_de_dados, carregar_dados
from chamadas import retorno_chamada, retorno_chamada_finetune
from constantes import (  # MODELO_FINAL,
    EPOCA_AJUSTE_FINO,
    EPOCA_TREINAMENTO_INICIAL,
    PASTA_MODELO,
    PASTA_TESTE,
    PASTA_TREINO,
    PASTA_VALIDACAO,
    ULTIMO_MODELO,
    ULTIMO_MODELO_AJUSTE,
)
from graficos import avaliacao, espacador, exibir_metricas, exibir_metricas_ajuste_fino
from modelo import criar_modelo_base, criar_modelo_fine
from recomendacao import criar_caracteristicas_extrator

# Limpar a memória e o cache do TensorFlow
tf.keras.backend.clear_session()
gc.collect()

# Verificar disponibilidade de TPU ou GPU e definir a estratégia de distribuição
try:
    tpu = tf.distribute.cluster_resolver.TPUClusterResolver()
    tf.config.experimental_connect_to_cluster(tpu)
    tf.tpu.experimental.initialize_tpu_system(tpu)
    estrategia = tf.distribute.TPUStrategy(tpu)
    # !pip install mlxtend
    print("TPU detectada e inicializada.")

except ValueError:
    estrategia = tf.distribute.get_strategy()
    if tf.config.list_physical_devices('GPU'):
        print(f"GPU detectada: {tf.config.list_physical_devices('GPU')}")
    else:
        print("Nenhuma GPU detectada. Usando CPU.\n")

# Carregar os dados de treino, teste e validação
dados_treino, dados_teste, dados_validacao = carregar_dados(PASTA_TREINO, PASTA_VALIDACAO, PASTA_TESTE)

# Cria o callback para o modelo MobileNetV2
checkpoint_MobileNetV2, lr_reduction, early_stopping = retorno_chamada(PASTA_MODELO)

# Cria o callback para o ajuste fino do modelo MobileNetV2
checkpoint_finetune, lr_reduction_fine, early_stopping_fine = retorno_chamada_finetune(PASTA_MODELO)

################################### MobileNetV2 #######################################

# Cria o modelo base MobileNetV2 e treina
modelo, modelo_base  = criar_modelo_base(estrategia, data_augmentation=aumentador_de_dados())

history = modelo.fit(
    dados_treino,
    validation_data=dados_validacao,
    epochs=EPOCA_TREINAMENTO_INICIAL,
    callbacks=[checkpoint_MobileNetV2, early_stopping, lr_reduction],
    )

# Avaliar o modelo com os dados de teste
avaliacao(modelo, dados_teste)

# Salvar o ultimo modelo treinado
modelo.save(f'{PASTA_MODELO}{ULTIMO_MODELO}')

# Exibir as métricas de treinamento do modelo
acc = [0.] + history.history['accuracy']
val_acc = [0.] + history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

espacador('MobileNetV2', 160)
exibir_metricas(acc, val_acc, loss, val_loss, 'MobileNetV2')

########################## Ajuste Fino MobileNetV2 ##################################

espacador('Ajuste Fino MobileNetV2', 160)
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

# Salvar o ultimo modelo treinado
modelo.save(f'{PASTA_MODELO}{ULTIMO_MODELO_AJUSTE}')

# Exibir as métricas de treinamento do modelo
acc += fine_tune_history.history['accuracy']
val_acc += fine_tune_history.history['val_accuracy']
loss += fine_tune_history.history['loss']
val_loss += fine_tune_history.history['val_loss']

espacador('Ajuste Fino MobileNetV2', 160)
exibir_metricas_ajuste_fino(acc, val_acc, loss, val_loss, epoca_inicial, 'Ajuste Fino MobileNetV2')

################################################################################

# Carrega as características dos produtos de treino e armazena em cache para o rapido acesso durante as consultas
espacador('Carregando Caracteristicas', 160)
modelo_extrator, cache_caracteristicas = criar_caracteristicas_extrator(PASTA_TREINO, modelo)

