# Projeto de criação de uma base de dados e treinamento da rede YOLOv4.
O trabalho deve conter pelo menos duas classes retreinadas para detecção, além das classes já treinadas previamente antes de realizar o transfer learning.

Por meio da imagem é possível visualizar um exemplo de resultado esperado:

![img](imagens/yolo.jpeg)

## Descrição
Este desafio consiste em adicionar mais duas classes a uma rede [YOLOv4](https://docs.ultralytics.com/pt/models/yolov4/#what-are-bag-of-freebies-in-the-context-of-yolov4) previamente treinada. As classes escolhidas são "abacate" e "chuchu".

## Conjunto de Dados
Utilizamos um pequeno conjunto de imagens contendo 100 fotos. Todas as imagens foram rotuladas utilizando a ferramenta [LabelImg](https://github.com/tzutalin/labelImg).

## Ferramentas Utilizadas
- [YOLOv4](https://docs.ultralytics.com/pt/models/yolov4/#what-are-bag-of-freebies-in-the-context-of-yolov4)
- [LabelImg](https://github.com/tzutalin/labelImg)

## Passos para Reproduzir
1. **Preparação do Ambiente**:
    - Instale as dependências necessárias.
    - Configure o ambiente para treinar a rede [YOLOv4](https://docs.ultralytics.com/pt/models/yolov4/#what-are-bag-of-freebies-in-the-context-of-yolov4).

2. **Rotulação das Imagens**:
    - Utilize o [LabelImg](https://github.com/tzutalin/labelImg) para rotular as imagens com as novas classes "abacate" e "chuchu".

    ![fig](imagens/l_img.JPG)

3. **Treinamento da Rede**:
    - Adicione as novas classes ao arquivo de configuração da [YOLOv4](https://docs.ultralytics.com/pt/models/yolov4/#what-are-bag-of-freebies-in-the-context-of-yolov4).
    - Treine a rede utilizando o conjunto de dados rotulado.

4. **Avaliação**:
    - Contagem de Detecções:
        - detections_count = 92: Número total de detecções feitas pela rede no conjunto de teste.
        - unique_truth_count = 34: Número total de objetos reais no conjunto de teste.
    - Resultados por Classe:
        - Abacate (class_id = 0):
            - AP (Average Precision): 76.83%
            - True Positives (TP): 12
            - False Positives (FP): 2
        - Chuchu (class_id = 1):
            - AP: 73.43%
            - TP: 13
            - FP: 4
        - Ambos os valores de AP são adequados para muitas aplicações, embora haja espaço para melhorias, especialmente na classe "chuchu".

    - Métricas Gerais:
        - Precision: 81% (precisão das detecções positivas).
        - Recall: 74% (cobertura de objetos reais identificados).
        - F1-score: 77% (balanceia precisão e recall).
        - IoU médio: 63.67% (média da sobreposição entre caixas previstas e reais).
        - mAP@0.50: 75.13% (desempenho global da rede para detecção com IoU ≥ 50%).
          
## Resultados
- No primeiro teste foi usado uma imagem contendo um elemento de cada classe, a rede não foi capaz de identificar corretamente o abacate, podemos ver que existe uma caixa de cada classe.

![teste1](imagens/teste1.png)

- Na segunda imagen de teste o resultado já foi melhor, as caixas delimitadoras ainda não esta cobrindo todo o chuchu, mas, por ter treinado apenas 900 épocas o resultado não esta ruim.

![teste2](imagens/teste2.png)

- Treceira imagem de teste, imagem apenas com abacates que foram bem detectados pela rede.

![teste3](imagens/teste3.png)

## Conclusão
- O modelo YOLOv4 apresenta um desempenho promissor com um mAP de 75.13% e bons indicadores de precisão e F1-score. Com ajustes e mais dados, pode-se melhorar a capacidade geral da rede para tarefas mais exigentes.
- A relação entre detections_count e unique_truth_count é importante para entender a precisão do modelo. Aqui, a precisão é de 81%, o que indica que a maioria das detecções feitas são úteis, mas ainda há 6 falsas detecções.

  
## Referências
- [YOLOv4 Paper](https://arxiv.org/abs/2004.10934)
- [LabelImg GitHub](https://github.com/tzutalin/labelImg)
