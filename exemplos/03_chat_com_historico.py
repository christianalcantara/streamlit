"""Etapa 3: o histórico sobrevive às reexecuções, sem chamar uma IA."""

import streamlit as st

st.title("Chat com histórico (sem IA)")
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

if st.button("Limpar conversa"):
    st.session_state.mensagens = []
    st.rerun()

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Digite uma mensagem")
if pergunta:
    resposta = f"Você escreveu: {pergunta}"
    for papel, texto in [("user", pergunta), ("assistant", resposta)]:
        st.session_state.mensagens.append({"role": papel, "content": texto})
        with st.chat_message(papel):
            st.markdown(texto)
