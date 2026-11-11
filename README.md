# Assistente de estudos com Streamlit e IA

Chatbot para revisar Python e eletricidade. O programa recebe perguntas, envia a conversa para a API Google Gemini e mostra a resposta conforme ela chega. Este projeto atende ao tema 4, nas páginas 11 e 12 da atividade de Informática Aplicada.

## Comece por aqui

O projeto foi pensado para iniciantes e para ser clonado do GitHub. Abra o [tutorial para iniciantes](tutorial/README.md) primeiro: ele ensina a baixar o projeto, instalar o Python e criar o chatbot passo a passo, com instruções principalmente para Windows.

O [roteiro de apresentação](docs/apresentacao.md) ajuda a preparar o seminário. O [plano de testes](docs/testes.md) orienta a demonstração e o registro dos resultados observados.

## Baixar e preparar no Windows

Instale o **Python 3.12 ou superior** e o **Git**. Durante a instalação do Python, marque a opção que adiciona Python ao `PATH`, se ela aparecer. Copie o endereço do repositório da equipe no GitHub e abra o Prompt de Comando.

Use o endereço verdadeiro do repositório nos comandos abaixo. O endereço exibido é apenas um exemplo:

```bat
cd %USERPROFILE%\Documents
git clone https://github.com/USUARIO/NOME-DO-REPOSITORIO.git
cd NOME-DO-REPOSITORIO
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install -r requirements.txt
```

Depois, configure a chave da API conforme a seção **Configurar a chave da API** abaixo e inicie o app:

```bat
python -m streamlit run streamlit_app.py
```

O navegador abrirá o chatbot. Para parar, volte ao Prompt de Comando e pressione `Ctrl+C`. No PowerShell, ative o ambiente com `.venv\Scripts\Activate.ps1`. Se preferir, o [tutorial](tutorial/README.md) explica os comandos um de cada vez e também traz instruções para baixar o ZIP pelo GitHub.

## Configurar a chave da API

1. Obtenha uma chave no [Google AI Studio](https://aistudio.google.com/apikey).
2. Na pasta do projeto, copie `.streamlit/secrets.toml.example` para `.streamlit/secrets.toml`.
3. Abra `secrets.toml` em um editor e preencha o campo da chave:

```toml
GEMINI_API_KEY = "cole-sua-chave-aqui"
GEMINI_MODEL = "gemini-3.5-flash-lite"
```

No Prompt de Comando do Windows, o comando para copiar é:

```bat
copy .streamlit\secrets.toml.example .streamlit\secrets.toml
```

**Nunca publique a chave no GitHub.** O Git ignora o arquivo `secrets.toml`; publique somente o arquivo de exemplo, que não contém uma chave válida. O arquivo de segredos não vai automaticamente dentro de um ZIP: confira antes de compartilhar a pasta. No Cloud, configure a chave na área de segredos do serviço.

## O que o projeto ensina

O tutorial inclui três pequenos programas que funcionam sem chave de IA. Depois, explica como a versão completa combina `streamlit_app.py` (tela e histórico) e `utils/gemini.py` (conversa com a API).

```text
tutorial/                 Aulas passo a passo para iniciantes
exemplos/                 Três programas curtos para praticar
streamlit_app.py          Tela do chatbot e histórico da conversa
utils/gemini.py           Envio de mensagens para a API Gemini
requirements.txt          Lista de bibliotecas instaladas com pip
.streamlit/
    secrets.toml.example  Exemplo de configuração sem chave secreta
docs/
    apresentacao.md       Roteiro do seminário
    testes.md             Plano e registro dos testes
tests/
    test_chatbot.py       Verificações automatizadas
```

## Verificações automatizadas

Com o ambiente `.venv` ativado, execute:

```bat
python -m unittest discover -s tests -v
```

Os testes foram feitos para funcionar sem chave e sem chamar a API. Para comprovar que a API real funciona, a equipe precisa iniciar o aplicativo com sua chave e fazer uma demonstração.

## Limitações

O histórico fica guardado temporariamente na sessão; fechar ou reiniciar o app pode apagá-lo. O serviço de IA precisa de internet, tem limites de uso e pode cometer erros. Confira as respostas técnicas com o material da aula. O chatbot responde por texto e não usa o PDF da tarefa como fonte de conhecimento.

## Referências

- [Python: criar ambientes virtuais](https://docs.python.org/pt-br/3/tutorial/venv.html)
- [Python: módulos](https://docs.python.org/pt-br/3/tutorial/modules.html)
- [Streamlit: conceitos principais](https://docs.streamlit.io/get-started/fundamentals/main-concepts)
- [Streamlit: construir um chatbot](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps)
- [Google Gen AI SDK para Python](https://googleapis.github.io/python-genai/)
- [Documentação da API Gemini](https://ai.google.dev/gemini-api/docs)
- [GitHub Docs](https://docs.github.com/pt)
