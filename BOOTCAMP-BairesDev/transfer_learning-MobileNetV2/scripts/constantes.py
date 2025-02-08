import os

NOME_CLASSES = {}
contador = 0

# Configurações gerais do sistema usadas no google colab
PASTA_ORIGINAL = '/content/drive/MyDrive/DIO/Projeto_Transfer_Learning/01-transfer_learning/Annonaceae'
PASTA_LOCAL = '/content/drive/MyDrive/DIO/Projeto_Transfer_Learning/01-transfer_learning'

MELHOR_MODELO = "melhor_modelo_MobileNetV2.keras"
ULTIMO_MODELO = "ultimo_modelo_MobileNetV2.keras"
MELHOR_MODELO_AJUSTE = "melhor_modelo_ajuste_fino.keras"
ULTIMO_MODELO_AJUSTE = "ultimo_modelo_ajuste_fino.keras"

PASTA_TREINO = f"{PASTA_LOCAL}/conjunto_dados/treino/"
PASTA_VALIDACAO = f"{PASTA_LOCAL}/conjunto_dados/validacao/"
PASTA_TESTE = f"{PASTA_LOCAL}/conjunto_dados/teste/"
PASTA_MODELO = f"{PASTA_LOCAL}/modelos/"

TAMANHO_IMG = (224, 224)
FORMA_ENTRADA = (224, 224, 3)
TAMANHO_DO_LOTE = 32
CAMADA_ESCONDIDA = 128
DROPOUT = 0.3
TAMANHO_FIGURA = (12, 5)

for raiz, dirs, arquivos in os.walk(PASTA_ORIGINAL):
    nome_pasta = os.path.basename(raiz).replace('_', ' ').title()
    if arquivos:
        NOME_CLASSES[contador] = nome_pasta
        contador += 1

NUM_CLASSE = len(NOME_CLASSES)
CLASSES = sorted(os.listdir(PASTA_TREINO))

EPOCA_TREINAMENTO_INICIAL = 15
TAXA_APRENDIZAGEM = 0.0001
TAXA_APRENDIZAGEM_AJUSTE = 0.00001
EPOCA_AJUSTE_FINO = 30
AJUSTE_FINO = 50
SEMENTE = 42
ESPACOS = 100
