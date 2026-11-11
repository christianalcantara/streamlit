"""Etapa 2: um chat de eco; ainda não usa API nem guarda histórico."""

import streamlit as st

st.title("Chat de eco (sem IA)")
pergunta = st.chat_input("Digite uma mensagem")
if pergunta:
    with st.chat_message("user"):
        st.markdown(pergunta)
    with st.chat_message("assistant"):
        st.markdown(f"Você escreveu: {pergunta}")
