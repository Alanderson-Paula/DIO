import os

NOME_CLASSES = {}
contador=0

# Configurações gerais do sistema usadas no google colab
PASTA_LOCAL='/pasta_local'
MELHOR_MODELO="melhor_modelo_MobileNetV2.keras"
ULTIMO_MODELO="ultimo_modelo_MobileNetV2.keras"
MELHOR_MODELO_AJUSTE="melhor_modelo_ajuste_fino.keras"
ULTIMO_MODELO_AJUSTE="ultimo_modelo_ajuste_fino.keras"
MODELO_FINAL="modelo_embeddings.keras"

PASTA_TREINO=f"{PASTA_LOCAL}/treino/"
PASTA_VALIDACAO=f"{PASTA_LOCAL}/validacao/"
PASTA_TESTE=f"{PASTA_LOCAL}/teste/"
PASTA_MODELO=f"{PASTA_LOCAL}/modelos/"

TAMANHO_IMG=(224, 224)
FORMA_ENTRADA=(224, 224, 3)
TAMANHO_DO_LOTE=32
CAMADA_ESCONDIDA=256
DROPOUT=0.1
TAMANHO_FIGURA=(12,8)

for raiz, dirs, arquivos in os.walk(PASTA_TREINO):
    nome_pasta = os.path.basename(raiz).replace('_', ' ').title()
    if arquivos:
        NOME_CLASSES[contador] = nome_pasta
        contador += 1

NUM_CLASSES=len(NOME_CLASSES)

EPOCA_TREINAMENTO_INICIAL=50
TAXA_APRENDIZAGEM=0.0001
EPOCA_AJUSTE_FINO=50
AJUSTE_FINO=50
SEMENTE=42
ESPACOS=100
