import os
import webbrowser

import requests
import speech_recognition as sr
from const import PASTA_AUDIOS, PASTA_TEXTOS
from conversor import converter_texto_em_audio, falar, salvar_fala_em_texto


def apresentacao():
    """
    Função que apresenta o sistema.
    """
    print("Iniciando o Sistema. Sistema 100% carregado e operando. Me chamo Paula.")
    falar("Iniciando o Sistema. Sistema 100% carregado e operando. Me chamo Paula.")


def ouvir_microfone():
    """
    Captura a fala do usuário através do microfone.
    Retorna a fala em formato de texto.
    Caso não seja possível ouvir, retorna None.

    :return: str ou None
    """
    microfone = sr.Recognizer()
    with sr.Microphone() as source:
        microfone.pause_threshold = 1
        microfone.energy_threshold = 300  # Adapta-se a ruídos ambientais.
        microfone.adjust_for_ambient_noise(source, duration=1)
        print("Aguardando comando...")
        audio = microfone.listen(source)
    try:
        frase = microfone.recognize_google(audio, language='pt-BR')
        return frase.lower()
    except sr.UnknownValueError:
        # print("Não entendi, pode repetir?")
        # falar("Não entendi, pode repetir?")
        return ""


def pesquisar_youtube(termo):
    """
    Abre uma busca no YouTube com o termo fornecido.
    Caso não seja possível acessar o YouTube, retorna None.

    :param termo: str contendo o termo de pesquisa
    """
    try:
        # Cria uma URL de pesquisa no YouTube
        query = "+".join(termo.split())
        url = f"https://www.youtube.com/results?search_query={query}"
        falar(f"Abrindo resultados de pesquisa para {termo} no YouTube.")
        webbrowser.open(url)
    except Exception as e:
        falar("Desculpe, não consegui acessar o YouTube.")
        print(f"Erro: {e}")


def pesquisar_local(nome):
    """
    Realiza uma pesquisa no Nominatim para obter informações de localização com base no nome fornecido.
    :param nome: str contendo o nome a ser pesquisado
    :return: str contendo as informações de localização ou uma mensagem de erro.

    """
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={nome}&format=json"
        response = requests.get(url, timeout=10)
        data = response.json()

        if data:
            # Nome completo da localização
            localizacao = data[0]["display_name"]
            return f"{nome} está localizada em: {localizacao}."
        else:
            return "Desculpe, não consegui encontrar informações sobre isso."
    except Exception as e:
        return f"Ocorreu um erro ao tentar buscar as informações para {nome}."


def executar_comando(frase):
    """
    Executa comandos baseados na fala.
    :param frase: str contendo a fala do usuário
    :return: None
    """
    if "abrir navegador" in frase:
        os.system("start chrome.exe")
        falar("Abrindo o navegador")

    elif "abrir calculadora" in frase:
        os.system("start calc.exe")
        falar("Abrindo a calculadora")

    elif "pesquisar" in frase:
        termo = frase.replace("pesquisar", "").strip()
        resultado = pesquisar_local(termo)
        falar(resultado)
        print(resultado)

    elif "salvar fala" in frase:
        falar("Diga algo que eu devo salvar como texto.")
        fala = ouvir_microfone()
        if fala:
            caminho_texto = salvar_fala_em_texto(fala, PASTA_TEXTOS)
            if caminho_texto:
                falar("Deseja que eu converta esse texto em áudio?")
                resposta = ouvir_microfone()
                if "sim" in resposta or "por favor" in resposta or "ok" in resposta:
                    falar("Convertendo o texto em áudio.")
                    converter_texto_em_audio(caminho_texto, PASTA_AUDIOS)

    elif "vídeo" in frase or "vídeos" in frase:
        termo = frase.replace("vídeo", "").replace("vídeos", "").strip()
        if termo:
            pesquisar_youtube(termo)
        else:
            falar("Por favor, diga o nome do vídeo que deseja buscar.")

    elif "desligar" in frase:
        falar("Desligando o sistema. Até logo.")
        os.system("exit")
        return True

    elif "sobre você" in frase:
        falar("Olá! Me chamo Paula, uma assistente virtual criada pelo Alanderson para o desafío de projeto da DIO.")
        return False

    else:
        falar(
            f"O comando '{frase}' não foi reconhecido, por favor tente novamente.")
    return False


apresentacao()

while True:
    ativacao = ouvir_microfone()
    if "ok paula" in ativacao:
        falar("Como posso te ajudar agora?")
        comando = ouvir_microfone()
        if comando:
            if executar_comando(comando):
                break
