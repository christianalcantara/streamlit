
"""Interface do chatbot. Execute: python -m streamlit run streamlit_app.py."""

# Bibliotecas instaladas pelo pip e um módulo criado por nós.
import os

import httpx
import streamlit as st
from google.genai import errors

from utils.gemini import MODELO_PADRAO, gerar_resposta

st.set_page_config(page_title="Assistente de estudos", page_icon=":material/school:")
st.title("Assistente de estudos", icon=":material/school:")
st.caption("Tire dúvidas de Python e eletricidade com respostas em tempo real.")


def ler_configuracao(nome: str, padrao: str = "") -> str:
    """Procura primeiro nos segredos do Streamlit, depois no ambiente."""
    try:
        valor = st.secrets.get(nome)
    except FileNotFoundError:
        valor = None  # É permitido executar sem um arquivo secrets.toml.
    return valor or os.getenv(nome) or padrao


# Uma variável comum seria recriada a cada interação. session_state mantém
# a conversa na memória desta sessão, mesmo quando o script roda novamente.
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

with st.sidebar:
    st.header("Sobre o projeto")
    st.markdown("**Python + Streamlit + API do Google Gemini**")
    st.caption("Projeto de Informática Aplicada. O histórico dura esta sessão.")
    modelo = ler_configuracao("GEMINI_MODEL", MODELO_PADRAO)
    st.caption(f"Modelo: {modelo}")
    if st.button("Limpar conversa", icon=":material/delete:"):
        st.session_state.mensagens = []
        st.rerun()  # Recomeça o script e redesenha a tela sem as mensagens.
    with st.expander("Como funciona?"):
        st.markdown(
            "1. Você envia uma pergunta.\n"
            "2. Python envia o histórico à API.\n"
            "3. A resposta chega em partes (streaming).\n"
            "4. A conversa fica guardada nesta sessão."
        )

chave = ler_configuracao("GEMINI_API_KEY") or ler_configuracao("GOOGLE_API_KEY")
if not chave:
    st.info(
        "Configure GEMINI_API_KEY em .streamlit/secrets.toml para começar. "
        "Consulte o README.md do projeto."
    )

# Cada mensagem é um dicionário; o histórico é uma lista desses dicionários.
for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input(
    "Ex.: explique a lei de Ohm com um exemplo",
    disabled=not chave,
    max_chars=2000,
    submit_mode="disable",  # Aguarda a resposta antes de aceitar outra pergunta.
)

if pergunta and pergunta.strip():
    nova_mensagem = {"role": "user", "content": pergunta.strip()}
    with st.chat_message("user"):
        st.markdown(nova_mensagem["content"])

    # + cria uma nova lista: só alteramos o histórico se a resposta terminar.
    historico = st.session_state.mensagens + [nova_mensagem]
    with st.chat_message("assistant"):
        saida = st.empty()  # Permite apagar uma resposta parcial se a conexão cair.
        try:
            with st.spinner("Aguardando a resposta..."):
                with saida.container():
                    resposta = st.write_stream(gerar_resposta(chave, modelo, historico))
            st.session_state.mensagens = historico + [
                {"role": "assistant", "content": resposta}
            ]
        except errors.APIError as erro:
            saida.empty()
            if erro.code in (400, 401, 403):
                st.error("Confira a chave da API e as permissões do projeto no Google AI Studio.")
            elif erro.code == 404:
                st.error("Modelo indisponível. Confira GEMINI_MODEL na configuração.")
            elif erro.code == 429:
                st.error("Cota ou limite de uso atingido. Verifique seu plano e tente mais tarde.")
            else:
                st.error("A API está indisponível. Tente novamente em instantes.")
        except httpx.HTTPError:
            saida.empty()
            st.error("Falha de conexão ou tempo de espera esgotado. Confira a internet e tente novamente.")
        except ValueError:
            saida.empty()
            st.error("Não foi possível obter uma resposta de texto. Reformule a pergunta e tente novamente.")
