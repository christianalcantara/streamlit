"""Etapa 1: python -m streamlit run exemplos/01_primeira_tela.py."""

# 'as st' dá um apelido à biblioteca que cria nossa interface.
import streamlit as st

st.title("Minha primeira aplicação")
nome = st.text_input("Qual é o seu nome?")
if nome:  # Só mostra a saudação quando o campo não está vazio.
    st.success(f"Olá, {nome}!")
