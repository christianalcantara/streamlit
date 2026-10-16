"""
Chatbot com Streamlit + Google Gemini (plano gratuito), com resposta em tempo real.

Como rodar:
    uv pip install streamlit google-genai
    export GEMINI_API_KEY="sua-chave-aqui" # gere em https://aistudio.google.com/apikey
    streamlit run chatbot_gemini.py

Opcional: trocar o modelo sem mexer no código
    export GEMINI_MODEL="gemini-3.8-flash"
"""

import os

import streamlit as st
from google import genai
from google.genai import errors, types

# Modelo rápido e econômico, recomendado pelo Google para projetos novos.
# Se der erro de modelo/cota, teste outro via variável GEMINI_MODEL.
MODELO = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
INSTRUCAO = "Você é um assistente prestativo. Responda em português do Brasil, de forma clara."

st.set_page_config(page_title="Chatbot", page_icon="🤖")
st.title("🤖 Chatbot")
st.caption(f"Modelo: {MODELO}")

# ---------------------------------------------------------------
# 1) Chave da API: variável de ambiente ou campo na barra lateral
# ---------------------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Chave da API do Gemini", type="password")
if not api_key:
    st.info("Informe a chave da API na barra lateral para começar.")
    st.stop()


@st.cache_resource
def get_client(chave: str) -> genai.Client:
    """Cria o cliente uma única vez (não a cada reexecução do script)."""
    return genai.Client(api_key=chave)


client = get_client(api_key)

# ---------------------------------------------------------------
# 2) Memória da conversa: session_state sobrevive às reexecuções.
#    Guardamos no formato simples {"role": "user"/"assistant", "content": ...}
# ---------------------------------------------------------------
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if st.sidebar.button("🗑️ Limpar conversa"):
    st.session_state.mensagens = []
    st.rerun()

# ---------------------------------------------------------------
# 3) Redesenha todo o histórico a cada execução do script
# ---------------------------------------------------------------
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ---------------------------------------------------------------
# 4) Converte o histórico para o formato do Gemini.
#    Diferença importante: no Gemini o papel da IA se chama "model",
#    não "assistant".
# ---------------------------------------------------------------
def para_formato_gemini(mensagens: list[dict]) -> list[types.Content]:
    return [
        types.Content(
            role="model" if m["role"] == "assistant" else "user",
            parts=[types.Part(text=m["content"])],
        )
        for m in mensagens
    ]


# ---------------------------------------------------------------
# 5) Função geradora: entrega a resposta pedaço por pedaço
# ---------------------------------------------------------------
def gerar_resposta():
    stream = client.models.generate_content_stream(
        model=MODELO,
        contents=para_formato_gemini(st.session_state.mensagens),
        config=types.GenerateContentConfig(system_instruction=INSTRUCAO),
    )
    for pedaco in stream:
        if pedaco.text:  # alguns pedaços podem vir vazios
            yield pedaco.text


# ---------------------------------------------------------------
# 6) Entrada do usuário
# ---------------------------------------------------------------
pergunta = st.chat_input("Digite sua mensagem...")

if pergunta:
    print(">>", pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.chat_message("assistant"):
        try:
            resposta = st.write_stream(gerar_resposta())
            st.session_state.mensagens.append({"role": "assistant", "content": resposta})
        except errors.APIError as erro:
            st.session_state.mensagens.pop()  # remove a pergunta sem resposta
            if erro.code == 429:
                st.error("Limite do plano gratuito atingido. Aguarde um minuto e tente de novo.")
            else:
                st.error(f"Erro ao chamar a API ({erro.code}): {erro.message}")