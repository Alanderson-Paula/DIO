import os

import cv2 as cv

pasta = os.getcwd()
print(pasta)

pasta_entrada = r'img_entrada\desconhecido'
pasta_saida = r'img_saida\WillSmith'


def main():
    contador = 1
    for nome_arquivo in os.listdir(f"{pasta}//{pasta_entrada}/"):
        if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.jfif')):
            novo_nome = "desconhecido" + str(contador) + ".jpg"
            nome_atual = f'{pasta}//{pasta_entrada}//' + nome_arquivo
            novo_nome = f'{pasta}//{pasta_entrada}//' + novo_nome
            contador += 1
            os.rename(nome_atual, novo_nome)

    # _resize()


def _resize():
    RESOLUCAO = (640, 640)
    caminho_pasta = f'{pasta}//{pasta_saida}/'

    for nome_arquivo in os.listdir(f"{pasta}//{pasta_entrada}/"):
        if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            nome_atual = f'{pasta}//{pasta_entrada}//' + nome_arquivo
            imagem = cv.imread(nome_atual, 1)
            imagem_reduzida = cv.resize(
                imagem, RESOLUCAO, interpolation=cv.INTER_CUBIC)
            cv.imwrite(os.path.join(caminho_pasta,
                       nome_arquivo), imagem_reduzida)


if __name__ == '__main__':
    main()
