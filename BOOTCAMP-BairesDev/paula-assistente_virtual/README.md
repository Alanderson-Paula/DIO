# Assistente Virtual `Paula`

Paula é uma assistente virtual interativa desenvolvida em Python que permite realizar diversas tarefas com comandos de voz, como abrir aplicativos, pesquisar no YouTube, salvar falas como texto e converter textos em áudios. Este projeto utiliza as bibliotecas `speech_recognition`, `pyttsx3`, e outras ferramentas embutidas no Python.

---

## Estrutura de Pastas

A organização do projeto é a seguinte:

```bash
/paula-assistente_virtual
|                |-- const.py      # constantes do projetos
|                |-- conversor.py  # Código dos conversores de fala e texto
|                |-- main.py       # Código principal da assistente
|-- textos/                        # Pasta para armazenar textos convertidos da fala
|-- audio/                         # Pasta para armazenar áudios gerados a partir dos textos
|-- README.md                      # Documentação do projeto
```

---

## Funcionalidades

1. **Abrir aplicativos**: Paula pode abrir aplicativos como navegador, calculadora, bloco de notas, Excel, Word, e Paint com comandos de voz.
2. **Pesquisar no YouTube**: Execute uma pesquisa no YouTube dizendo o que deseja assistir.
3. **Salvar fala como texto**: Converta sua fala em um arquivo `.txt` e salve automaticamente na pasta `textos/`.
4. **Converter texto em áudio**: Transforme textos salvos em arquivos de áudio `.mp3` na pasta `audio/`.
5. **Interação personalizada**: A assistente responde apenas após o comando de ativação: `OK Paula!`.

---

## Dependências

Certifique-se de instalar as seguintes bibliotecas antes de executar o projeto:

- `pyttsx3`: Para conversão de texto em fala.
- `speech_recognition`: Para reconhecimento de voz.

Você pode instalá-las com o seguinte comando:
```bash
pip install pyttsx3 SpeechRecognition
```

---

## Requisitos do Sistema

- **Python 3.7 ou superior**: O projeto foi testado com Python 3.11.5.
- **Sistema operacional compatível**: Windows (para os comandos de abertura de aplicativos como Excel e Word).
- **Microfone**: Necessário para captar comandos de voz.

### Configuração adicional
- **Permissões de microfone**: Certifique-se de que o microfone está configurado corretamente no sistema operacional.
- **Pastas necessárias**: As pastas `textos/` e `audio/` serão criadas automaticamente na primeira execução.

---

## Como Executar

1. Clone ou baixe o repositório.
2. Navegue até a pasta do projeto.
3. Execute o script principal:
   ```bash
   python main.py
   ```
4. Após a mensagem de inicialização, ative a assistente com o comando `OK Paula!`.
5. Use os comandos disponíveis para interagir com a assistente.

---

## Exemplos de Uso

### Abrir aplicativos
- **Comando:** `OK Paula, abrir navegador.`
- **Ação:** A assistente abrirá o navegador Chrome.

### Pesquisar no YouTube
- **Comando:** `OK Paula, abrir vídeo de gatos engraçados.`
- **Ação:** A assistente abrirá a pesquisa no YouTube com o termo "gatos engraçados".

### Salvar fala como texto
- **Comando:** `OK Paula, salvar fala.`
- **Ação:** A assistente solicitará algo para você dizer e salvará como arquivo de texto em `textos/`.

### Converter texto em áudio
- **Comando:** Após salvar um texto, a assistente perguntará: `Deseja que eu converta esse texto em áudio?`
- **Ação:** Se você responder "sim", "ok" ou "por favor" o texto será convertido em áudio na pasta `audios/`.

---

## Melhorias Futuras


1. **Lista de comandos dinâmica**: Criar um arquivo contendo uma lista de comandos reconhecidos e permite ao usuário:

   - **Consultar comandos disponíveis**:
      - **Comando:** `OK Paula, listar comandos.`
      - **Ação:** A assistente recitará os comandos disponíveis.

   - **Adicionar novo comando**:
      - **Comando:** `OK Paula, adicionar comando abrir câmera.`
      - **Ação:** O comando "abrir câmera" será adicionado à lista de comandos reconhecidos.

   - **Remover comando existente**:
      - **Comando:** `OK Paula, remover comando abrir câmera.`
      - **Ação:** O comando "abrir câmera" será removido da lista de comandos reconhecidos.

2. **Aprimorar reconhecimento de voz**: Implementar modelos mais avançados de reconhecimento de fala para maior precisão, como integração com APIs externas (e.g., Google Cloud Speech-to-Text).
3. **Integração com serviços de pesquisa**: Adicionar funcionalidades para buscar informações mais detalhadas na web, como localização, horários de funcionamento e descrições de locais.
4. **Feedback por texto**: Permitir que os usuários vejam no console ou em um arquivo log o comando reconhecido para validar interações.
5. **Personalização de comandos**: Desenvolver uma interface gráfica simples para gerenciar a lista de comandos de maneira visual, além do comando de voz.
6. **Integração com IoT**: Expandir as funcionalidades para controle de dispositivos inteligentes, como lâmpadas ou outros equipamentos IoT.

---
