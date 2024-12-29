# Projeto: Reconhecimento de Imagens com MTCNN

---

## Parte 1 - Introdução ao Reconhecimento de Imagens com MTCNN

O reconhecimento de imagens é uma das áreas mais impactantes da visão computacional. Essa tecnologia permite identificar e classificar objetos, rostos e padrões visuais com alta precisão. Uma das bibliotecas mais populares para reconhecimento facial é a **MTCNN (Multi-task Cascaded Convolutional Networks)**. Neste projeto, exploraremos o uso da MTCNN de forma prática, abordando desde a configuração inicial até aplicações avançadas.

### O que é a MTCNN?
A MTCNN é uma rede neural convolucional projetada para realizar detecção de rostos, alinhamento facial e extração de pontos-chave. Ela opera em três estágios hierárquicos:
1. **Proposal Network (P-Net):** Responsável por gerar regiões candidatas para rostos.
2. **Refine Network (R-Net):** Refina as regiões propostas e reduz falsos positivos.
3. **Output Network (O-Net):** Realiza a detecção final e marca pontos-chave, como olhos, nariz e boca.

### Matemática por Trás do MTCNN
A biblioteca utiliza convoluções para extrair características em diferentes estágios:
- **Convoluções:** Aplicam filtros para identificar padrões visuais.
- **ReLU:** Função de ativação para modelar não-linearidades.
- **Pooling:** Reduz a dimensionalidade e preserva características relevantes.
- **Classificação e Regressão:** Usa funções softmax e de perda para classificar e ajustar previsões.

---

## Parte 2 - Configuração e Instalação

### Requisitos:
- **Python 3.6+**
- **Bibliotecas auxiliares:** TensorFlow ou Keras, NumPy, OpenCV, Sklearn e Matplotlib.

### Passo 1: Instalação
```bash
pip install mtcnn
pip install tensorflow
pip install opencv-python matplotlib numpy
```

### Passo 2: Testando a Instalação
```python
from mtcnn import MTCNN
import cv2
import matplotlib.pyplot as plt

detector = MTCNN()
print("Instalação bem-sucedida!")
```

---

## Parte 3 - Implementação Básica: Detecção de Rostos

### 1. Código para Detecção de Rostos em Imagens
```python
import cv2
from mtcnn import MTCNN
import matplotlib.pyplot as plt

# Função para exibir resultados
def exibir_resultado(imagem, faces):
    fig, ax = plt.subplots()
    ax.imshow(imagem)

    for face in faces:
        x, y, largura, altura = face['box']
        pontos = face['keypoints']

        # Desenhar retângulo
        ax.add_patch(plt.Rectangle((x, y), largura, altura, edgecolor='red', facecolor='none'))

        # Marcar pontos-chave
        for ponto in pontos.values():
            ax.plot(ponto[0], ponto[1], 'bo')

    plt.axis('off')
    plt.show()

# Carregar imagem
def detectar_rostos(caminho_imagem):
    imagem = cv2.cvtColor(cv2.imread(caminho_imagem), cv2.COLOR_BGR2RGB)
    detector = MTCNN()
    faces = detector.detect_faces(imagem)
    exibir_resultado(imagem, faces)

# Executar detecção
detectar_rostos('exemplo.jpg')
```

### 2. Explicação do Código:
- **Carregamento de imagem:** Usa OpenCV para processar imagens no formato RGB.
- **Detecção de rostos:** Identifica regiões faciais e pontos-chave.
- **Visualização:** Desenha caixas delimitadoras e marcações para facilitar a análise visual.

---

## Parte 4 - Aplicações

### 1. Alinhamento Facial
Este processo utiliza os pontos-chave para ajustar a orientação do rosto:
```python
import numpy as np

def alinhar_rosto(imagem, pontos):
    olho_esquerdo = pontos['left_eye']
    olho_direito = pontos['right_eye']

    # Calcular ângulo de rotação
    delta_x = olho_direito[0] - olho_esquerdo[0]
    delta_y = olho_direito[1] - olho_esquerdo[1]
    angulo = np.degrees(np.arctan2(delta_y, delta_x))

    # Alinhar a imagem
    centro = tuple(np.mean([olho_esquerdo, olho_direito], axis=0).astype(int))
    matriz = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    imagem_alinhada = cv2.warpAffine(imagem, matriz, (imagem.shape[1], imagem.shape[0]))
    return imagem_alinhada
```

### 2. Reconhecimento Facial com Embeddings
Integração com modelos como **FaceNet**:
```python
from keras_facenet import FaceNet

embedder = FaceNet()
embedding = embedder.embeddings([imagem_alinhada])
print(embedding)
```

### 3. Detecção em Tempo Real
```python
cap = cv2.VideoCapture(0)
detector = MTCNN()

while True:
    ret, frame = cap.read()
    imagem = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector.detect_faces(imagem)

    for face in faces:
        x, y, largura, altura = face['box']
        cv2.rectangle(frame, (x, y), (x+largura, y+altura), (0, 255, 0), 2)

    cv2.imshow('Detecção em Tempo Real', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

### 4. Processamento de Vídeos
Processamento frame a frame semelhante ao código acima, permitindo análise de grandes conjuntos de dados.

---

## Conclusão
Este projeto apresentou um guia completo para detecção de rostos usando a biblioteca MTCNN, cobrindo desde configurações básicas até técnicas avançadas. Ele pode ser expandido para sistemas de autenticação, segurança e análise emocional, adaptando-se facilmente a diferentes cenários. Se precisar de mais exemplos ou adaptações, avise-nos!




### Saidas

Maju Coutinho

![img1](image_saida\maju.JPG)

Will Smith

![img1](image_saida\will.JPG)
