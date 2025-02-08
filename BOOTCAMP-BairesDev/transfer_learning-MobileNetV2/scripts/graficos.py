import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.metrics import auc, classification_report, confusion_matrix, roc_curve

from constantes import CLASSES, ESPACOS, NOME_CLASSES, TAMANHO_FIGURA


# Função para exibir as métricas de treinamento
def exibir_metricas(acc, val_acc, loss, val_loss, nome_modelo) -> None:
    """
    ##### Exibir as métricas de treinamento do modelo
    Arguemntos:
        acc: Precisão no treinamento
        val_acc: Precisão na validação
        loss: Perda no treinamento
        val_loss: Perda na validação
        nome_modelo: Nome do modelo

    Retorna:  None
        """
    fig = plt.figure(figsize=(14,5))

    # Plotar a acurácia
    ax = fig.add_subplot(1, 2, 1)
    ax.plot(acc, label='Precisão no treinamento')
    ax.plot(val_acc, label='Precisão na validação')
    ax.legend(loc='lower right')
    ax.set_ylabel('Precisão')
    ax.set_ylim([min(ax.set_ylim()), 1])
    ax.set_title(f'Precisão de treinamento e validação {nome_modelo}')
    ax.set_xlabel('época')

    # Plotar a perda (loss)
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(loss, label='Perda de treinamento')
    ax2.plot(val_loss, label='Perda de validação')
    ax2.legend(loc='upper right')
    ax2.set_ylabel('Entropia Cruzada')
    ax2.set_ylim([0, 1.0])
    ax2.set_title(f'Perda de treinamento e validação {nome_modelo}')
    ax2.set_xlabel('época')

    plt.show()


# Função para exibir as métricas de treinamento
def exibir_metricas_ajuste_fino(acc, val_acc, loss, val_loss, epoca_inicial, nome_modelo) -> None:
    """
    ##### Exibir as métricas de treinamento do modelo
    Arguemntos:
        acc: Precisão no treinamento
        val_acc: Precisão na validação
        loss: Perda no treinamento
        val_loss: Perda na validação
        epoca_inicial: Época inicial do ajuste fino
        nome_modelo: Nome do modelo
    Retorna:  None
        """
    fig = plt.figure(figsize=(12, 8))

    # Plotar a acurácia
    plt.subplot(2, 1, 1)
    plt.plot(acc, label='Precisão no treinamento')
    plt.plot(val_acc, label='Precisão na validação')
    plt.ylim([0, 1])
    plt.plot([epoca_inicial-1, epoca_inicial-1],
             plt.ylim(), label='Inicio do ajuste fino')
    plt.legend(loc='lower right')
    plt.title(f'Precisão de treinamento e validação {nome_modelo}')

    plt.subplot(2, 1, 2)
    plt.plot(loss, label='Perda de treinamento')
    plt.plot(val_loss, label='Perda de validação')

    plt.ylim([0, 1.0])
    plt.plot([epoca_inicial-1, epoca_inicial-1],
             plt.ylim(), label='Inicio do ajuste fino')
    plt.legend(loc='upper right')
    plt.title(f'Perda de treinamento e validação {nome_modelo}')
    plt.xlabel('época')

    plt.show()


# Função para adicionar um separador visual
def espacador(titulo: str = None, largura_total: int = ESPACOS):
    """
    #### Adiciona um separador visual com um título opcional.

    Argumentos:
        titulo: Título do separador
        largura_total: Largura total do separador (padrão: 160)

    Retorna: None
    """
    if titulo is not None:
        tamanho_titulo = len(titulo)
        espacos_laterais = (largura_total - tamanho_titulo - 2) // 2
        espacos_restantes = largura_total - \
            (espacos_laterais * 2) - tamanho_titulo - 2
        print("\n" + "#" * espacos_laterais +
              f" {titulo} " + "#" * (espacos_laterais + espacos_restantes) + "\n")
    else:
        print("\n" + "#" * largura_total + "\n")


# Função para avaliar o modelo
def avaliacao(modelo, dados_teste):
    """
    #### Avalia o modelo com os dados de teste.

    Argumentos:
        modelo: Modelo treinado
        dados_teste: Dados de teste

   Retorno:
        - Exibe a perda (loss) e a acurácia no teste
    """
    espacador('🔹 Avaliação do Modelo')
    test_loss, test_acc = modelo.evaluate(dados_teste)

    print(f"\n🔹 Perda no Teste: {test_loss:.4f}")
    print(f"🔹 Acurácia no Teste: {test_acc:.4f}")

    espacador('🔹 Relatório de Classificação')
    # Previsões e relatório
    y_true = np.concatenate([y.numpy() for _, y in dados_teste])
    y_pred_prob = modelo.predict(dados_teste)
    y_pred = np.argmax(y_pred_prob, axis=1)

    print("\nRelatório de Classificação:")
    print(classification_report(y_true, y_pred,
          target_names=NOME_CLASSES.values()))

    # Exibir Matriz de Confusão
    espacador('🔹 Matriz de Confusão')
    exibir_matriz_confusao(y_true, y_pred)
    print('\n')
    # return test_loss, test_acc


# Função para exibir previsões
def exibir_array_previsoes(idx, y_pred, dataset_teste):
    """
    Exibe a imagem e a previsão do modelo para um índice fornecido pelo usuário.

    Argumentos:
        - idx (int): Índice da imagem a ser exibida.
        - y_pred (array): Array de previsões do modelo.
        - dataset_teste (tf.data.Dataset): Dataset contendo as imagens e rótulos reais.
    """

    imagens, rotulos = [], []

    # Percorre todos os lotes do dataset e armazena imagens e rótulos
    for lote_imagens, lote_rotulos in dataset_teste:
        imagens.extend(lote_imagens.numpy())
        rotulos.extend(lote_rotulos.numpy())

    # Converter listas para arrays NumPy
    imagens = np.array(imagens)
    rotulos = np.array(rotulos)

    # Verificar se o índice fornecido é válido
    if idx < 0 or idx >= len(imagens):
        print(f"⚠️ Índice inválido! Escolha um número entre 0 e {len(imagens) - 1}.")
        return

    # Obter a imagem e o rótulo real
    imagem = imagens[idx]
    rotulo_real = rotulos[idx]

    # Processar imagem para exibição
    imagem = (imagem + 1) * 127.5  # Normalizar de [-1,1] para faixa de 0 a 255
    imagem = imagem.astype("uint8")

    # Obter a previsão do modelo
    rotulo_predito = np.argmax(y_pred[idx])
    cor_titulo = "blue" if rotulo_predito == rotulo_real else "red"

    # Criar a figura com a imagem e gráfico de barras
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=TAMANHO_FIGURA)

    # Exibir a imagem com a previsão
    ax1.imshow(imagem)
    ax1.text(0.5, -0.01, f"{NOME_CLASSES[rotulo_predito]} {100*np.max(y_pred[idx]):2.0f}% ({NOME_CLASSES[rotulo_real]})",
             color=cor_titulo, ha="center", va="top", transform=ax1.transAxes, fontsize=12)
    ax1.axis("off")

    # Criar patches para legenda
    patch_real = mpatches.Patch(color="blue", label="Confiança na Classe Certa")
    patch_predita = mpatches.Patch(color="red", label="Confiança na Classe Errada")

    # Criar gráfico de barras das probabilidades posiciona a legenda ao lado da barra de menor probabilidade
    y_pred_prob = y_pred[idx]
    if y_pred_prob[0] > y_pred_prob[1]:
        legenda_posicao = "upper right"
    else:
        legenda_posicao = "upper left"

    color_barras = ["blue" if i == rotulo_real else "red" for i in range(len(NOME_CLASSES))]
    bars = ax2.bar(NOME_CLASSES.values(), y_pred_prob, color=color_barras)

    ax2.set_ylim([0, 1])
    ax2.set_ylabel('Probabilidade')
    ax2.set_title('Distribuição do Modelo por Classe')
    ax2.legend(handles=[patch_real, patch_predita], loc=legenda_posicao)

    # Adicionar porcentagem em cada barra garantindo que o texto não ultrapasse o topo
    for bar in bars:
        altura = bar.get_height()
        posicao_texto = min(altura + 0.001, 0.95)
        ax2.text(bar.get_x() + bar.get_width() / 2, posicao_texto, f'{altura*100:.2f}%',
                 ha='center', va='bottom', color='black', fontsize=10)

    plt.tight_layout()
    plt.show()


# Função para exibir matriz de confusão
def exibir_matriz_confusao(y_true, y_pred):
    """
    #### Plota a Matriz de Confusão do modelo.

    Argumentos:
        - y_true: Rótulos verdadeiros
        - y_pred (array): Array de previsões do modelo

    """
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=NOME_CLASSES.values(),
                yticklabels=NOME_CLASSES.values())
    plt.xlabel("Predito")
    plt.ylabel("Real")
    plt.title("Matriz de Confusão")
    plt.show()


# exibir a curvo ROC
def plotar_curva_roc(y_true, y_pred_prob):
    """
    #### Plota a Curva ROC do modelo.

    Argumentos:
        - y_true: Rótulos verdadeiros
        - y_pred_prob: Probabilidades preditas da classe positiva (1)
    """
    # Calcular a Curva ROC e a AUC
    fpr, tpr, _ = roc_curve(y_true, y_pred_prob[:, 1])  # Pegamos a probabilidade da classe 1
    roc_auc = auc(fpr, tpr)

    # Plotar a Curva ROC
    plt.figure(figsize=(6, 5))
    plt.plot(fpr, tpr, color="blue", lw=2, label=f"Área sob a curva (AUC) = {roc_auc:.2f}")
    plt.plot([0, 1], [0, 1], color="gray", linestyle="--")  # Linha de referência
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel("Taxa de Falsos Positivos (FPR)")
    plt.ylabel("Taxa de Verdadeiros Positivos (TPR)")
    plt.title("Curva ROC")
    plt.legend(loc="lower right")
    plt.grid()
    plt.show()


# Função para plotar a distribuição das classes
def plotar_distribuicao_classes(contagem_original):
    """
    #### Plota a distribuição das classes.
    """
    labels = list(contagem_original.keys())
    categorias = [CLASSES[i] for i in labels]

    valores_originais = [contagem_original[i] for i in labels]

    x = range(len(categorias))

    plt.figure(figsize=(6, 5))
    bars = plt.bar(x, valores_originais, width=0.5, label='Original', align='center', alpha=0.7, color='blue')

    for bar in bars:
        altura = bar.get_height()
        posicao_texto = min(altura + 0.001, 0.95)
        plt.text(bar.get_x() + bar.get_width() / 2, posicao_texto,
                 f'{int(altura)}', ha='center', va='bottom', fontsize=12, color='black')#, fontweight='bold')

    plt.xlabel("Classes")
    plt.ylabel("Número de imagens")
    plt.title("Distribuição das Classes")
    plt.xticks(x, categorias, rotation=0)
    plt.legend()
    plt.show()
