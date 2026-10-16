import json
from itertools import chain

import streamlit as st
from google.genai import errors

from utils.gemini import gerar_resposta, obter_chave_api, obter_cliente, obter_modelo

PERSONALIDADES = {
    "Prestativo": "Você é um assistente prestativo. Responda em português do Brasil, de forma clara.",
    "Professor": (
        "Você é um professor paciente. Explique em português do Brasil, passo a passo, "
        "com exemplos simples."
    ),
    "Divertido": (
        "Você é um assistente bem-humorado. Responda em português do Brasil, "
        "com leveza e algumas piadas."
    ),
}

SUGESTOES = {
    ":blue[:material/help:] O que é Streamlit?": "Explique o que é o Streamlit em poucas linhas.",
    ":green[:material/code:] Exemplo de código": "Mostre um exemplo simples de app em Streamlit.",
    ":orange[:material/lightbulb:] Ideia de projeto": "Sugira uma ideia de projeto escolar usando Python.",
}

modelo = obter_modelo()

# ---------------------------------------------------------------
# Estado da conversa: session_state sobrevive às reexecuções
# ---------------------------------------------------------------
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# ---------------------------------------------------------------
# Barra lateral: configurações do chat
# ---------------------------------------------------------------
with st.sidebar:
    st.header("Configurações do chat", divider="gray")

    api_key = obter_chave_api()
    if not api_key:
        api_key = st.text_input(
            "Chave da API do Gemini",
            type="password",
            help="Gere gratuitamente em https://aistudio.google.com/apikey",
        )

    personalidade = st.radio(
        "Personalidade",
        list(PERSONALIDADES)
    )
    temperatura = st.slider(
        "Criatividade (temperature)",
        min_value=0.0,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Valores maiores deixam as respostas mais variadas.",
    )

    # Reservamos o espaço agora e preenchemos no fim do script,
    # para que os botões já considerem a última resposta.
    acoes = st.container(horizontal=True)

st.caption(f"Modelo: `{modelo}` · Personalidade: **{personalidade}**")

if not api_key:
    st.info(
        "Informe a chave da API na barra lateral para começar.",
        title="Chave da API necessária",
        icon=":material/key:",
    )
    st.stop()

cliente = obter_cliente(api_key)

# ---------------------------------------------------------------
# Redesenha o histórico a cada execução do script
# ---------------------------------------------------------------
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------
# Entrada do usuário (digitada ou via sugestão)
# ---------------------------------------------------------------
pergunta = st.chat_input("Digite sua mensagem...", submit_mode="disable")

if not st.session_state.mensagens:
    sugestoes = st.empty()
    escolhida = sugestoes.pills("Experimente perguntar:", list(SUGESTOES), label_visibility="collapsed")
    if escolhida:
        pergunta = SUGESTOES[escolhida]
    if pergunta:
        sugestoes.empty()

def com_spinner(gerador, texto="Pensando..."):
    """Mostra um spinner até o primeiro pedaço chegar e devolve o stream completo."""
    with st.spinner(texto):
        primeiro = next(gerador, "")  # bloqueia até a API começar a responder
    return chain([primeiro], gerador)


def mostrar_erro(erro: errors.APIError):
    if erro.code == 429:
        st.error(
            "Limite do plano gratuito atingido. Aguarde um minuto e tente de novo.",
            icon=":material/hourglass_empty:",
        )
    else:
        st.error(f"Erro ao chamar a API ({erro.code}): {erro.message}", icon=":material/error:")

if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        try:
            stream = com_spinner(
                gerar_resposta(
                    cliente,
                    modelo,
                    st.session_state.mensagens,
                    PERSONALIDADES[personalidade],
                    temperatura,
                )
            )
            resposta = st.write_stream(stream)
            st.session_state.mensagens.append({"role": "assistant", "content": resposta})
        except errors.APIError as erro:
            st.session_state.mensagens.pop()  # remove a pergunta sem resposta
            mostrar_erro(erro)

if st.session_state.mensagens and st.session_state.mensagens[-1]["role"] == "assistant":
    st.feedback(
        "thumbs",
        key=f"feedback_{len(st.session_state.mensagens)}",
        on_change=lambda: st.toast("Obrigado pelo feedback!", icon=":material/favorite:"),
    )

with acoes:
    if st.button("Limpar", icon=":material/delete:", disabled=not st.session_state.mensagens):
        st.session_state.mensagens = []
        st.rerun()
    st.download_button(
        "Baixar",
        data=json.dumps(st.session_state.mensagens, ensure_ascii=False, indent=2),
        file_name="conversa.json",
        mime="application/json",
        icon=":material/download:",
        disabled=not st.session_state.mensagens,
        on_click="ignore",
    )
