import os
from datetime import datetime

import pyttsx3

engine = pyttsx3.init()

def falar(texto):
    """
    Função que permite falar.
    """
    engine.say(texto)
    engine.runAndWait()


def converter_texto_em_audio(caminho_texto, pasta_audio):
    """
    #### Converte o conteúdo de um arquivo de texto em áudio e salva na pasta audio/.

    Caso não seja possível converter, retorna None.

    :param caminho_texto: str contendo o caminho do arquivo de texto
    :param pasta_textos: str contendo o caminho da pasta de audio
    :return: None
    """
    try:
        if not os.path.exists(pasta_audio):
            os.makedirs(pasta_audio)
        with open(caminho_texto, "r", encoding="utf-8") as file:
            conteudo = file.read()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_audio = f"{pasta_audio}audio_{timestamp}.mp3"
        engine.save_to_file(conteudo, arquivo_audio)
        engine.runAndWait()
        print(f"Áudio salvo em {arquivo_audio}")
        falar("O áudio foi gerado e salvo com sucesso.")
    except Exception as e:
        print(f"Erro ao converter texto em áudio: {e}")
        falar("Houve um erro ao tentar gerar o áudio.")


def salvar_fala_em_texto(fala, pasta_texto):
    """
    #### Salva a fala em um arquivo de texto na pasta textos/.

    Retorna o nome do arquivo. Caso não seja possível salvar, retorna None.

    :param fala: str contendo a fala a ser salva em texto
    :param pasta_textos: str contendo o caminho da pasta de texto
    :return: str or None

    """
    try:
        if not os.path.exists(pasta_texto):
            os.makedirs(pasta_texto)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo_texto = f"{pasta_texto}fala_{timestamp}.txt"
        with open(arquivo_texto, "w", encoding="utf-8") as file:
            file.write(fala)
        print(f"Fala salva em {arquivo_texto}")
        falar(f"Sua fala foi salva como texto com o nome {arquivo_texto}")
        return arquivo_texto
    except Exception as e:
        print(f"Erro ao salvar texto: {e}")
        falar("Houve um erro ao tentar salvar sua fala como texto.")
        return None
